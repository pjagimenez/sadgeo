#!/usr/bin/env bash
# Requires Bash, curl and Python 3. No Oracle writes: --crud is accepted only in demo.
set -euo pipefail
umask 077
BASE_URL="${1:-http://127.0.0.1:8080}"
BASE_URL="${BASE_URL%/}"
CRUD=false
if [[ "${2:-}" == "--crud" ]]; then CRUD=true; fi
TMP_DIR="$(mktemp -d)"
CREATED=false
TEST_CODE=''
CSRF_HEADER=''
CSRF_TOKEN=''
request() {
  local method="$1" path="$2" expected="$3" file="${4:-}" status
  local args=(--silent --show-error --connect-timeout 10 --max-time 60 --cookie "$TMP_DIR/cookies" --cookie-jar "$TMP_DIR/cookies" --request "$method" --output "$TMP_DIR/response.json" --write-out '%{http_code}')
  if [[ "$method" != GET ]]; then args+=(--header "$CSRF_HEADER: $CSRF_TOKEN"); fi
  if [[ -n "$file" ]]; then args+=(--header "Content-Type: ${5:-application/json}" --data-binary "@$file"); fi
  status="$(curl "${args[@]}" "$BASE_URL$path")"
  if [[ "$status" != "$expected" ]]; then
    printf 'FAIL %s %s: HTTP %s; esperado %s\n' "$method" "$path" "$status" "$expected" >&2
    cat "$TMP_DIR/response.json" >&2
    return 1
  fi
}
csrf() {
  request GET /api/auth/csrf 200
  mapfile -t csrf_parts < <(python3 - "$TMP_DIR/response.json" <<'PY'
import json,sys
x=json.load(open(sys.argv[1]));print(x['headerName']);print(x['token'])
PY
)
  CSRF_HEADER="${csrf_parts[0]}"; CSRF_TOKEN="${csrf_parts[1]}"
}
cleanup() {
  if $CREATED; then
    csrf && request DELETE /api/tabelas/localizacao 204 "$TMP_DIR/delete.json" || true
  fi
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT
request GET /actuator/health 200
request GET /api/dashboard/config 200
DEMO="$(python3 -c 'import json,sys;print(str(json.load(open(sys.argv[1]))["demo"]).lower())' "$TMP_DIR/response.json")"
if $CRUD && [[ "$DEMO" != true ]]; then echo '--crud só é permitido em demo; o script não altera Oracle real.' >&2; exit 1; fi
request GET /api/dashboard/resumo 200
request GET /api/registros/critica 401
csrf
if [[ "$DEMO" == true ]]; then
  request POST /api/auth/demo 200
else
  read -r -p 'Login da rede: ' TEST_USER
  read -r -s -p 'Senha da rede: ' TEST_PASSWORD; printf '\n'
  printf '%s\0%s' "$TEST_USER" "$TEST_PASSWORD" | python3 -c 'import sys,urllib.parse;u,p=sys.stdin.buffer.read().decode().split("\0",1);sys.stdout.write(urllib.parse.urlencode({"username":u,"password":p}))' > "$TMP_DIR/login.form"
  unset TEST_PASSWORD
  request POST /api/auth/login 200 "$TMP_DIR/login.form" application/x-www-form-urlencoded
  rm -f "$TMP_DIR/login.form"
fi
request GET /api/auth/me 200
request GET /api/dashboard/resumo 200
request GET /api/registros/critica 200
for item in altimetria:medA gravimetria:medG planimetria:medP vrf:vrf veg:veg ogr:ogr gabinete:gab; do
  context="${item%%:*}"; campaign="${item#*:}"
  request GET "/api/registros/$context?size=100&campanha=tentativa-de-troca" 200
  python3 - "$TMP_DIR/response.json" "$campaign" "$DEMO" <<'PY'
import json,sys
x=json.load(open(sys.argv[1]));assert x['campanha']==sys.argv[2]
assert all(r['campanha']==sys.argv[2] for r in x['items'])
if sys.argv[3]=='true':assert x['total']>0,'Demo deve conter registros para cada campanha'
PY
  printf 'OK filtro %s = %s\n' "$context" "$campaign"
done
request GET "/api/registros/critica?size=999" 400
request GET /api/registros/desconhecido 404
request GET /api/tabelas 200
request GET /api/tabelas/localizacao 200
python3 - "$TMP_DIR/response.json" <<'PY'
import json,sys
x=json.load(open(sys.argv[1]));assert x['meta']['keys']==['TIPO_LOCAL']
PY
request GET /api/tabelas/campanha/meta 200
python3 - "$TMP_DIR/response.json" <<'PY'
import json,sys
assert set(json.load(open(sys.argv[1]))['keys'])=={'COD_CAMPANHA','COD_PROJETO','COD_INSTITUICAO'}
PY
request GET /api/tabelas/pendencia 200
if $CRUD; then
  # Find an unused code; never overwrite or delete an existing record.
  for candidate in Z9 Z8 Z7 Z6 Z5 Z4 Z3 Z2 Z1 Z0; do
    request GET "/api/tabelas/localizacao?q=$candidate" 200
    count="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["total"])' "$TMP_DIR/response.json")"
    if [[ "$count" == 0 ]]; then TEST_CODE="$candidate"; break; fi
  done
  if [[ -z "$TEST_CODE" ]]; then echo 'Nenhum código livre para o teste.' >&2; exit 1; fi
  printf '{"TIPO_LOCAL":"%s","DESCRICAO":"Teste automatizado"}' "$TEST_CODE" > "$TMP_DIR/create.json"
  printf '{"key":{"TIPO_LOCAL":"%s"},"values":{"DESCRICAO":"Teste atualizado"}}' "$TEST_CODE" > "$TMP_DIR/update.json"
  printf '{"key":{"TIPO_LOCAL":"%s"}}' "$TEST_CODE" > "$TMP_DIR/delete.json"
  csrf; request POST /api/tabelas/localizacao 201 "$TMP_DIR/create.json"; CREATED=true
  csrf; request PUT /api/tabelas/localizacao 200 "$TMP_DIR/update.json"
  request GET "/api/tabelas/localizacao/item?TIPO_LOCAL=$TEST_CODE" 200
  python3 -c 'import json,sys;assert json.load(open(sys.argv[1]))["DESCRICAO"]=="Teste atualizado"' "$TMP_DIR/response.json"
  csrf; request DELETE /api/tabelas/localizacao 204 "$TMP_DIR/delete.json"; CREATED=false
  request GET "/api/tabelas/localizacao/item?TIPO_LOCAL=$TEST_CODE" 404
  echo 'OK CRUD Localização (demo), com limpeza do registro criado'
fi
csrf; request POST /api/auth/logout 204
request GET /api/dashboard/resumo 200
request GET /api/registros/critica 401
echo 'PASS: saúde, login, sessão, dashboard, campanhas, catálogos e logout'
