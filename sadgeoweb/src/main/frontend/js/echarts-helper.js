// echarts-helper.js

window.SadgeoCharts = {

    init(chartId, option) {

		console.log(
		    "ECHART ID",
		    chartId
		);
		console.log(
		    "ECHART OPTION",
		    option
		);
		
		const element =
		        document.getElementById(chartId);
				
		const chart =
		        echarts.init(element);

		    option = eval('(' + option + ')');

		    chart.setOption(option);

		    window[chartId + "_instance"] =
		        chart;

		    new ResizeObserver(() => {

		        chart.resize();

		    }).observe(element);
    },

    resizeAll() {

        Object.keys(window)

            .filter(k =>
                k.endsWith("_instance"))

            .forEach(k => {

                const chart =
                    window[k];

                if (chart) {

                    chart.resize();
                }
            });
    },
	
	update(chartId, option) {

        const chart =
            window[chartId + "_instance"];

		if (!chart) {
		   return;
		}

		if (typeof option === 'string') {
            option = eval('(' + option + ')');
        }

        chart.setOption(
            option,
            true
        );
    }
};

window.addEventListener(
    'resize',
    () => window.SadgeoCharts.resizeAll()
);