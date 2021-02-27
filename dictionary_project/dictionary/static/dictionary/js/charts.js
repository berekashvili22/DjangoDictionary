function totalData(data){
    var totalDicts = document.getElementById('totalDicts')
    var totalWords = document.getElementById('totalWords')
    var totalQuizes = document.getElementById('totalQuizes')

    totalDicts.innerHTML = data['total']['dicts']
    totalWords.innerHTML = data['total']['words']
    totalQuizes.innerHTML = data['total']['quizes']
}

function buildDateCharts(data) {

    var dateLabels = data['dateLabels']

    var wordsByDateValues = data['words_by_date']['values']
    var dictsByDateValues = data['dicts_by_date']['values']
    var quizesByDateValues = data['quizes_by_date']['values']

    // chart 1
    var chartData = {
        'type':'bar',
        'backgroundColor':'none', // This is in the root
        'plotarea':{
            backgroundColor:'transparent'
        },
        'plot': {
            backgroundColor: '#4b5a72',
        },
        'title': {
            text: 'New words',
            fontSize: 18,
            fontColor: '#854125',
        },
        'scale-x':{
            'values': dateLabels,
            'item': {
                'font-color': '#854125',
            },
        },
        'series':[
            {
                'values': wordsByDateValues,
            }
        ],
        'scale-y':{

            'item': {
                'font-color': '#854125',
            },

        },
    }

    zingchart.render({
        id:'myChart',
        data: chartData,
    })

    // chart 2

    var chartData1 = {
        'type':'bar',
        'backgroundColor':'none', // This is in the root
        'plotarea':{
            backgroundColor:'transparent'
        },
        'plot': {
            backgroundColor: '#4b5a72',
            // styles: ["#3f3f3f", "#cc99ff", "#cc99ff", "#cc99ff"]
        },
        'title': {
            text: 'New dictionaries',
            fontSize: 18,
            fontColor: '#854125',
        },
        'scale-x':{
            'values': dateLabels,
            'item': {
                'font-color': '#854125',
            },
        },
        'series':[
            {
                'values': dictsByDateValues,
            }
        ],
        'scale-y':{

            'item': {
                'font-color': '#854125',
            },

        },

    }

    zingchart.render({
        id:'myChart1',
        data: chartData1,
    })


    // chart 2

    var chartData2 = {
        'type':'bar',
        'backgroundColor':'none', // This is in the root
        'plotarea':{
            backgroundColor:'transparent'
        },
        'plot': {
            backgroundColor: '#4b5a72',
            // styles: ["#3f3f3f", "#cc99ff", "#cc99ff", "#cc99ff"]
        },
        'title': {
            text: 'New quizes',
            fontSize: 18,
            fontColor: '#854125',
        },
        'scale-x':{
            'values': dateLabels,
            'item': {
                'font-color': '#854125',
            },
        },
        'series':[
            {
                'values': quizesByDateValues,
            }
        ],
        'scale-y':{

            'item': {
                'font-color': '#854125',
            },

        },

    }

    zingchart.render({
        id:'myChart2',
        data: chartData2,
    })
}

function buildQuizScoreCharts(data) {
    
    var avgMonth = data['avgScoreByMonth']
    console.log(avgMonth)

    let chartConfig4 = {
    type: 'area',
    stacked: true,
    title: {
        text: 'Monthly Average Score',
        fontColor: '#3f3f3f'
    },
    subtitle: {
        text: 'Quiz Results',
        // fontColor: '#cb8670'
        fontColor: '#cb8670'
    },
    plot: {
        activeArea: true,
        animation: {
        delay: 50,
        effect: 'ANIMATION_SLIDE_LEFT',
        method: 'ANIMATION_REGULAR_EASE_OUT',
        sequence: 'ANIMATION_NO_SEQUENCE',
        speed: 1500
        },
        hoverMarker: {
        size: '8px'
        }
    },
    plotarea: {
        backgroundColor: '#fff'
    },
    scaleX: {
        lineColor: '#333',
        labels: ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'],
    },
    scaleY: {
        minValue: 0,
        maxValue: 100,
        item: {
        padding: '2px'
        },
        lineColor: '#333',
        tick: {
        lineColor: '#333'
        }
    },
    series: [
        {
        values: [
            avgMonth['Jan.'],
            avgMonth['Feb.'],
            avgMonth['Mar.'],
            avgMonth['Apr.'],
            avgMonth['May'],
            avgMonth['June'],
            avgMonth['July'],
            avgMonth['Aug.'],
            avgMonth['Sept.'],
            avgMonth['Oct.'],
            avgMonth['Nov.'],
            avgMonth['Dec.']
        ],
        backgroundColor: 'rgba(11, 201, 11, 0.400)',
        lineColor: 'green',
        marker: {
            backgroundColor: 'green',
            borderColor: '#fff',
            borderWidth: '2px'
        }
        },
    ]
    };

    zingchart.render({
    id: 'myChart4',
    data: chartConfig4,
    });
    
 
}

