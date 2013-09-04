var pieChart;
var animatedPie;
var doubleAxisBars;

window.onload = function () {
  
  /*********** PIE CHARTS *******************/
  var elements = [
    {
      percentage: 50,
      color: '#CDBFE0',
      text: '50 Facebook',
      x: 150,
      y: 130
    },
    {
      percentage: 30,
      color: '#6845C7',
      text: '30 Twitter',
      x: 150,
      y: 150
    },
    {
      percentage: 20,
      color: '#975EE3',
      text: '20 Linkedin',
      x: 150,
      y: 170
    }
  ];
  
  var r_1_1 = Raphael('canvas_1_1', 400, 400);
  animatedPie = new EdAnimatedPie(r_1_1, elements, {
    animationTime: 900,
    easing: '<',
    useAnimationDelay: false,
    lineWidth: 70,
    fontSize: 20,
    centerx: 200,
    centery: 200,
    radius: 100,
    drawReferences: false
  });
  animatedPie.draw();
  
  var elements = [
    {
      percentage: 50,
      color: '#D44B5F',
      text: '50 Facebook',
      x: 150,
      y: 130
    },
    {
      percentage: 30,
      color: '#DC6666',
      text: '30 Twitter',
      x: 150,
      y: 150
    },
    {
      percentage: 20,
      color: '#FF836F',
      text: '20 Linkedin',
      x: 150,
      y: 170
    }
  ];
  var r_1_2 = Raphael('canvas_1_2', 400, 400);
  animatedPie = new EdAnimatedPie(r_1_2, elements, {
    animationTime: 900,
    easing: '<',
    useAnimationDelay: false,
    lineWidth: 70,
    fontSize: 20,
    centerx: 200,
    centery: 200,
    radius: 100,
    drawReferences: false
  });
  animatedPie.draw();
  
  /*********** DOT CHARTS *******************/
  var r_2_1 = Raphael('canvas_2_1', 210, 210);
  dotChart = new EdDotChart(r_2_1, [
    {
      radius: 100,
      color: '#E26667',
      label: '225'
    },
    {
      radius: 60,
      color: '#704DA0',
      label: '134'
    }
  ], {
    centerx: 100,
    centery: 101,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false
  });
  dotChart.draw();
  
  var r_2_2 = Raphael('canvas_2_2', 210, 210);
  dotChart = new EdDotChart(r_2_2, [
    {
      radius: 100,
      color: '#F6F6F6'
    },
    {
      radius: 80,
      color: '#704DA0'
    },
    {
      radius: 20,
      color: '#E26667'
    }
  ], {
    centerx: 100,
    centery: 101,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false
  });
  dotChart.draw();
  
  var r_2_3 = Raphael('canvas_2_3', 210, 210);
  dotChart = new EdDotChart(r_2_3, [
    {
      radius: 100,
      color: '#F6F6F6'
    },
    {
      radius: 60,
      color: '#E26667'
    },
    {
      radius: 30,
      color: '#704DA0'
    }
  ], {
    centerx: 100,
    centery: 101,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false
  });
  dotChart.draw();
  
  var r_2_4 = Raphael('canvas_2_4', 210, 210);
  dotChart = new EdDotChart(r_2_4, [
    {
      radius: 100,
      color: '#F6F6F6'
    },
    {
      radius: 40,
      color: '#704DA0'
    },
    {
      radius: 30,
      color: '#E26667'
    }
  ], {
    centerx: 100,
    centery: 101,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false
  });
  dotChart.draw();
  
  /*********** QUARTER PIE *******************/
  var elements = [
    {
      percentage: 8,
      color: '#6845C7',
      text: 'Master'
    },
    {
      percentage: 10,
      color: '#6845C7',
      text: 'Phd and above'
    },
    {
      percentage: 23,
      color: '#6845C7',
      text: 'Under graduate programs'
    },
    {
      percentage: 5,
      color: '#E56666',
      text: 'Technical institute'
    },
    {
      percentage: 3,
      color: '#6845C7',
      text: 'Highschool'
    },
    {
      percentage: 57,
      color: '#6845C7',
      text: 'Junior College'
    },
    {
      percentage: 3,
      color: '#6845C7',
      text: 'Primary School'
    }
  ];
  
  var r_3_1 = Raphael('canvas_3_1', 435, 428);
  animatedPie = new EdQuarterAnimatedPie(r_3_1, elements, {
    animationTime: 900,
    easing: '<',
    useAnimationDelay: false,
    lineWidth: 45,
    fontSize: 20,
    centerx: 435,
    centery: 430,
    radius: 400,
    drawReferences: false
  });
  animatedPie.draw();
  
  /*********** BAR CHARTS *******************/
  var r_4_1 = Raphael('canvas_4_1', 1093, 423);
  doubleAxisBars = new EdBarChart(r_4_1, {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: false,
    drawLabels: true,
    elements: [
      {pos: 20, width: 200, color: '#6C47A7', value: 70},
      {pos: 230, width: 100, color: '#E56666', value: 120},
      {pos: 330, width: 100, color: '#6C47A7', value: 80},
      {pos: 440, width: 200, color: '#6C47A7', value: 140},
      {pos: 650, width: 200, color: '#6C47A7', value: 200},
      {pos: 860, width: 200, color: '#6C47A7', value: 100},
    ],
    xAxis: {
      length: 1093,
      labels: [
        {pos: 110, text: '15-25', type: 'normal'},
        {pos: 320, text: '25-35', type: 'normal'},
        {pos: 540, text: '35-45', type: 'normal'},
        {pos: 740, text: '45-55', type: 'normal'},
        {pos: 950, text: '55-65', type: 'normal'}
      ]
    },
    yAxis: {
      length: 423,
      labels: [
        {pos: 90, text: '01', width: 1090, type: 'dotted'},
        {pos: 180, text: '10', width: 1090, type: 'dotted'},
        {pos: 270, text: '20', width: 1090, type: 'dotted'},
        {pos: 360, text: '30', width: 1090, type: 'dotted'}
      ]
    },
    centerx: 30,
    centery: 400,
    canvasSize: [1093,423]
  });
  doubleAxisBars.draw();
};