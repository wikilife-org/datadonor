var pieChart;
var animatedPie;
var doubleAxisBars;
var animatedQuarterPie;
var doubleAxisParams;

window.onload = function () {
  
  /*********** PIE CHARTS *******************/
  var elements = [
    {
      percentage: 50,
      color: '#6845C7',
      text: '50',
      x: 150,
      y: 130,
      image: {
        path: '/static/img/img/iconos/1_face.png',
        width: '26',
        height: '20',
        offsetx: '-13',
        offsety: '-20'
      }
    },
    {
      percentage: 40,
      color: '#975EE3',
      text: '30',
      x: 150,
      y: 150,
      image: {
        path: '/static/img/img/iconos/3_linke.png',
        width: '26',
        height: '20',
        offsetx: '-13',
        offsety: '-20'
      }
    },
    {
      percentage: 10,
      color: '#CDBFE0',
      text: '20',
      x: 150,
      y: 170,
      image: {
        path: '/static/img/img/iconos/4_mail.png',
        width: '26',
        height: '20',
        offsetx: '-13',
        offsety: '-20'
      }
    }
  ];
  
  var r_1_1 = Raphael('canvas_1_1', 410, 410);
  animatedPie = new EdAnimatedPie(r_1_1, elements, {
    animationTime: 900,
    easing: '<',
    useAnimationDelay: false,
    lineWidth: 70,
    fontSize: 20,
    centerx: 200,
    centery: 200,
    radius: 100,
    borderColor: '#DCDDDD',
    drawReferences: true,
    drawCenterImage: true,
    bubbleColor: '#3F4B5B',
    text: {
      color: '#ADB6BF',
      size: '18'
    },
    centerImage: {
      width: 60,
      height: 84,
      x: 168,
      y: 160,
      path: '/static/img/img/iconos/overall_avg.png'
    }
  });
  animatedPie.draw();
  
  var elements = [
    {
      percentage: 50,
      color: '#D44B5F',
      text: '50',
      x: 150,
      y: 130,
      image: {
        path: '/static/img/img/iconos/1_face.png',
        width: '26',
        height: '20',
        offsetx: '-13',
        offsety: '-20'
      }
    },
    {
      percentage: 30,
      color: '#DC6666',
      text: '30',
      x: 150,
      y: 150,
      image: {
        path: '/static/img/img/iconos/3_linke.png',
        width: '26',
        height: '20',
        offsetx: '-13',
        offsety: '-20'
      }
    },
    {
      percentage: 20,
      color: '#FF836F',
      text: '200',
      x: 150,
      y: 170,
      image: {
        path: '/static/img/img/iconos/4_mail.png',
        width: '26',
        height: '20',
        offsetx: '-13',
        offsety: '-20'
      }
    }
  ];
  var r_1_2 = Raphael('canvas_1_2', 410, 410);
  animatedPie2 = new EdAnimatedPie(r_1_2, elements, {
    animationTime: 900,
    easing: '<',
    useAnimationDelay: false,
    lineWidth: 70,
    fontSize: 20,
    centerx: 200,
    centery: 200,
    radius: 100,
    borderColor: '#DCDDDD',
    drawReferences: true,
    drawCenterImage: true,
    bubbleColor: '#E56666',
    text: {
      color: 'white',
      size: '18'
    },
    centerImage: {
      width: 67,
      height: 74,
      x: 167,
      y: 160,
      path: '/static/img/img/iconos/your_avg.png'
    }
  });
  animatedPie2.draw();
  
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
    centerx: 105,
    centery: 101,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false,
    perimeter: {
      display: false
    }
  });
  dotChart.draw();
  
  var r_2_2 = Raphael('canvas_2_2', 210, 210);
  dotChart = new EdDotChart(r_2_2, [
//    {
//      radius: 100,
//      color: '#F6F6F6'
//    },
    {
      radius: 80,
      color: '#704DA0'
    },
    {
      radius: 20,
      color: '#E26667'
    }
  ], {
    centerx: 105,
    centery: 103,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false,
    perimeter: {
      display: true,
      radius: 100,
      color: '#ECEDED'
    }
  });
  dotChart.draw();
  
  var r_2_3 = Raphael('canvas_2_3', 210, 210);
  dotChart = new EdDotChart(r_2_3, [
//    {
//      radius: 100,
//      color: '#F6F6F6'
//    },
    {
      radius: 60,
      color: '#E26667'
    },
    {
      radius: 30,
      color: '#704DA0'
    }
  ], {
    centerx: 105,
    centery: 103,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false,
    perimeter: {
      display: true,
      radius: 100,
      color: '#ECEDED'
    }
  });
  dotChart.draw();
  
  var r_2_4 = Raphael('canvas_2_4', 210, 210);
  dotChart = new EdDotChart(r_2_4, [
//    {
//      radius: 100,
//      color: '#F6F6F6'
//    },
    {
      radius: 40,
      color: '#704DA0'
    },
    {
      radius: 30,
      color: '#E26667'
    }
  ], {
    centerx: 105,
    centery: 103,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false,
    perimeter: {
      display: true,
      radius: 102,
      color: '#ECEDED'
    }
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
      color: '#6845C7',
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
  animatedQuarterPie = new EdQuarterAnimatedPie(r_3_1, elements, {
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
  animatedQuarterPie.draw();
  
  /*********** BAR CHARTS *******************/
  var r_4_1 = Raphael('canvas_4_1', 1093, 423);
  doubleAxisParams = {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: true,
    drawLabels: true,
    elements: [
      {pos: 20, width: 200, color: '#6C47A7', value: 70, label: "20"},
      {pos: 230, width: 100, color: '#E56666', value: 120, label: "40"},
      {pos: 330, width: 100, color: '#6C47A7', value: 80, label: "50"},
      {pos: 440, width: 200, color: '#6C47A7', value: 140, label: "60"},
      {pos: 650, width: 200, color: '#6C47A7', value: 200, label: "70"},
      {pos: 860, width: 200, color: '#6C47A7', value: 100, label: "80"},
    ],
    xAxis: {
      length: 1093,
      "stroke-width": 2,
      color: '#F1F2F2',
      labels: [
        {pos: 110, text: '15-25', type: 'normal', "font-size": 20, "font-family": 'Verdana'},
        {pos: 320, text: '25-35', type: 'normal', "font-size": 20, "font-family": 'Verdana'},
        {pos: 540, text: '35-45', type: 'normal', "font-size": 20, "font-family": 'Verdana'},
        {pos: 740, text: '45-55', type: 'normal', "font-size": 20, "font-family": 'Verdana'},
        {pos: 950, text: '55-65', type: 'normal', "font-size": 20, "font-family": 'Verdana'}
      ]
    },
    yAxis: {
      length: 423,
      "stroke-width": 0,
      name: 'years',
      labels: [
        {pos: 90, text: '01', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F1F2F2', "text-color": "#ADB6BF"},
        {pos: 180, text: '10 years avg', width: 1090, type: 'dotted', "stroke-width": 3, color: '#6C53C3', "text-color": "#6C53C3"},
        {pos: 270, text: '20', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F1F2F2', "text-color": "#ADB6BF"},
        {pos: 360, text: '30', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F1F2F2', "text-color": "#ADB6BF"}
      ]
    },
    centerx: 30,
    centery: 400,
    canvasSize: [1093,425]
  }
  doubleAxisBars = new EdBarChart(r_4_1, doubleAxisParams);
  doubleAxisBars.draw();
};

$(document).ready(function(){
  $('#your_lvl_c li a').click(function (event) {
    var pos = $(this).attr('ref');
    //line = animatedQuarterPie.lines[pos];
    for(var i in animatedQuarterPie.lines){
      line = animatedQuarterPie.lines[i];
      if(pos == i){
        line.animate({"stroke": '#E56666'}, 500);
      }else{
        line.animate({"stroke": animatedQuarterPie.colors[i]}, 500);
      }
    }
  });
  
  $('#age_select_form').submit(function(){
    console.log('form submitted!');
    var age = $('#age_select_value').val();
    $('#canvas_4_1').html('');
    var r_4_1 = Raphael('canvas_4_1', 1093, 423);
    doubleAxisParams.elements[1].value = 140;
    doubleAxisBars = new EdBarChart(r_4_1, doubleAxisParams);
    doubleAxisBars.draw();
    return false;
  });
});