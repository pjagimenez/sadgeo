package br.gov.ibge.geodesia.sadgeo.catalogo;

import java.util.Map;
import org.springframework.dao.*;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestControllerAdvice(assignableTypes = CatalogController.class)
public class CatalogErrors {
  @ExceptionHandler(ResponseStatusException.class)
  ResponseEntity<?> status(ResponseStatusException e) {
    return ResponseEntity.status(e.getStatusCode())
        .body(Map.of("message", e.getReason() == null ? "Requisição inválida" : e.getReason()));
  }

  @ExceptionHandler(DuplicateKeyException.class)
  ResponseEntity<?> duplicate() {
    return ResponseEntity.status(409)
        .body(Map.of("message", "Já existe um registro com essa chave"));
  }

  @ExceptionHandler(DataIntegrityViolationException.class)
  ResponseEntity<?> integrity() {
    return ResponseEntity.status(409)
        .body(
            Map.of(
                "message",
                "Operação rejeitada pelas restrições do banco (campos, chave ou referências)"));
  }

  @ExceptionHandler(DataAccessException.class)
  ResponseEntity<?> unavailable() {
    return ResponseEntity.status(503)
        .body(
            Map.of(
                "message",
                "Não foi possível acessar a tabela. Verifique objetos e permissões no Oracle"));
  }
}
