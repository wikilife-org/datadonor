var pieChart;
var animatedPie;
var doubleAxisBars;
var animatedQuarterPie;
var doubleAxisParams;

function drawSocialGraph(elments1, elements2){
	  var r_1_1 = Raphael('canvas_1_1', 410, 410);
	  animatedPie = new EdAnimatedPie(r_1_1, elments1, {
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
	      path: '/static/img/iconos/overall_avg.png'
	    }
	  });
	  animatedPie.draw();

	  
	  var r_1_2 = Raphael('canvas_1_2', 410, 410);
	  animatedPie2 = new EdAnimatedPie(r_1_2, elements2, {
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
	      path: '/static/img/iconos/your_avg.png'
	    }
	  });
	  animatedPie2.draw();
}

function drawShareGraphs(){
  var adapter = new SocialShareAdapter();
  var graphConfig = {
    centerx: 105,
    centery: 101,
    useAnimationDelay: true,
    animationTime: 900,
    easing: 'bounce',
    fontSize: '40',
    drawLabels: false,
    perimeter: {
      display: false,
      radius: 100,
      color: '#ECEDED'
    }
  };
    
  var maxPercentage = 80;
  var elements1 = adapter.getParameters([data.global_data.facebook.posts, data.user_data.facebook.posts], maxPercentage, 100);
  var r_2_1 = Raphael('canvas_2_1', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  
  dotChart = new EdDotChart(r_2_1, elements1, graphConfig);
  dotChart.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([data.global_data.twitter.tweets, data.user_data.twitter.tweets], maxPercentage, 100);
  var r_2_2 = Raphael('canvas_2_2', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;

  dotChart2 = new EdDotChart(r_2_2, elements1, graphConfig);
  dotChart2.draw();
}

window.onload = function () {
  
  /*********** PIE CHARTS *******************/
	$.getJSON( "../../static/js/adapter/examples/social_reach", function( data ) {
    console.log(data);
    var adapter = new SocialReachAdapter();
    var elements1 = adapter.getParameters(data.global_data, ['#CDBFE0','#6845C7','#975EE3','#CDBFE0','#975EE3']);
    var elements2 = adapter.getParameters(data.user_data, ['#D44B5F','#DC6666','#FF836F','#D44B5F','#DC6666']);
    console.log(elements1); console.log(elements2);
    drawSocialGraph(elements1, elements2)
  });
  
  $.getJSON( "../../static/js/adapter/examples/share", function( data ) {
    drawShareGraphs(data);
  });
  
  
  /*********** DOT CHARTS *******************/
  
  
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
  
  var r_5_1 = Raphael('canvas_5_1', 210, 210);
  dotChart = new EdDotChart(r_5_1, [
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
  
  var r_5_2 = Raphael('canvas_5_2', 210, 210);
  dotChart = new EdDotChart(r_5_2, [
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
  
  var r_5_3 = Raphael('canvas_5_3', 210, 210);
  dotChart = new EdDotChart(r_5_3, [
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
  
  var r_6_1 = Raphael('canvas_6_1', 1093, 423);
  doubleAxisParams2 = {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: true,
    drawLabels: true,
    elements: [
      {pos: 30, width: 62, color: '#6C47A7', value: 250, label: "2000", vlabel: "20"},
      {pos: 92, width: 62, color: '#E56666', value: 300, label: "4000", vlabel: "20"},
      {pos: 174, width: 62, color: '#6C47A7', value: 80, label: "500", vlabel: "20"},
      {pos: 236, width: 62, color: '#E56666', value: 140, label: "60"},
      {pos: 318, width: 62, color: '#6C47A7', value: 200, label: "70"},
      {pos: 380, width: 62, color: '#E56666', value: 100, label: "80"},
      {pos: 462, width: 62, color: '#6C47A7', value: 200, label: "70"},
      {pos: 524, width: 62, color: '#E56666', value: 100, label: "80"},
      {pos: 606, width: 62, color: '#6C47A7', value: 200, label: "70"},
      {pos: 668, width: 62, color: '#E56666', value: 100, label: "80"},
      {pos: 750, width: 62, color: '#6C47A7', value: 200, label: "70"},
      {pos: 812, width: 62, color: '#E56666', value: 100, label: "80"},
      {pos: 894, width: 62, color: '#6C47A7', value: 200, label: "70"},
      {pos: 956, width: 62, color: '#E56666', value: 100, label: "80"}
    ],
    xAxis: {
      length: 1093,
      "stroke-width": 2,
      color: '#F1F2F2',
      labelsType: 'custom_bubbles',
      name: 'Day',
      labels: [
        {pos: 92, text: 'S', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 236, text: 'M', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 380, text: 'T', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 524, text: 'W', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 668, text: 'T', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 812, text: 'F', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 956, text: 'S', type: 'bubble', "font-size": 20, "font-family": 'Verdana'}
      ]
    },
    yAxis: {
      length: 423,
      "stroke-width": 0,
      name: 'Steps',
      labels: [
        {pos: 90, text: '', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F1F2F2', "text-color": "#ADB6BF"},
        {pos: 300, text: '150\navg', width: 1090, type: 'dotted', "stroke-width": 3, color: '#6C53C3', "text-color": "#6C53C3", "font-size": 13},
        {pos: 150, text: '72\navg', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F0ACAC', "text-color": "#F0ACAC", "font-size": 13},
        {pos: 180, text: '', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F1F2F2', "text-color": "#ADB6BF"},
        {pos: 270, text: '', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F1F2F2', "text-color": "#ADB6BF"},
        {pos: 360, text: '', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F1F2F2', "text-color": "#ADB6BF"}
      ]
    },
    centerx: 30,
    centery: 400,
    canvasSize: [1093,425]
  }
  doubleAxisBars2 = new EdBarChart(r_6_1, doubleAxisParams2);
  doubleAxisBars2.draw();
  
  var r_7_1 = Raphael('canvas_7_1', 530, 400);
  doubleAxisParams3 = {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: true,
    drawLabels: true,
    elements: [
      {pos: 30, width: 45, color: '#6C47A7', value: 250, label: "2000"},
      {pos: 45, width: 45, color: '#E56666', value: 300, label: "4000"},
      {pos: 100, width: 45, color: '#6C47A7', value: 80, label: "500"},
      {pos: 115, width: 45, color: '#E56666', value: 140, label: "60"},
      {pos: 170, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 185, width: 45, color: '#E56666', value: 100, label: "80"},
      {pos: 240, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 255, width: 45, color: '#E56666', value: 100, label: "80"},
      {pos: 310, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 325, width: 45, color: '#E56666', value: 100, label: "80"},
      {pos: 385, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 400, width: 45, color: '#E56666', value: 100, label: "80"},
      {pos: 455, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 470, width: 45, color: '#E56666', value: 100, label: "80"}
    ],
    xAxis: {
      length: 1093,
      "stroke-width": 2,
      color: '#E6E2DF',
      labelsType: 'custom_bubbles',
      labels: [
        {pos: 60, text: 'S', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 130, text: 'M', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 200, text: 'T', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 270, text: 'W', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 340, text: 'T', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 415, text: 'F', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 485, text: 'S', type: 'bubble', "font-size": 20, "font-family": 'Verdana'}
      ]
    },
    yAxis: {
      length: 423,
      "stroke-width": 0,
      name: 'years',
      labels: [
        {pos: 300, text: '50\navg', width: 1090, type: 'dotted', "stroke-width": 3, color: '#6C53C3', "text-color": "#6C53C3", "font-size": 13},
        {pos: 150, text: '27\navg', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F0ACAC', "text-color": "#F0ACAC", "font-size": 13},
        {pos: 90, text: '10', width: 1090, type: 'dotted', "stroke-width": 3, color: '#E6E2DF', "text-color": "#ADB6BF"},
        {pos: 180, text: '30', width: 1090, type: 'dotted', "stroke-width": 3, color: '#E6E2DF', "text-color": "#ADB6BF"},
        {pos: 270, text: '40', width: 1090, type: 'dotted', "stroke-width": 3, color: '#E6E2DF', "text-color": "#ADB6BF"}
      ]
    },
    centerx: 10,
    centery: 370,
    canvasSize: [530,400]
  }
  doubleAxisBars3 = new EdBarChart(r_7_1, doubleAxisParams3);
  doubleAxisBars3.draw();
  
  var r_7_2 = Raphael('canvas_7_2', 530, 400);
  doubleAxisParams4 = {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: true,
    drawLabels: true,
    elements: [
      {pos: 30, width: 45, color: '#6C47A7', value: 250, label: "2000"},
      {pos: 45, width: 45, color: '#E56666', value: 300, label: "4000"},
      {pos: 100, width: 45, color: '#6C47A7', value: 80, label: "500"},
      {pos: 115, width: 45, color: '#E56666', value: 140, label: "60"},
      {pos: 170, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 185, width: 45, color: '#E56666', value: 100, label: "80"},
      {pos: 240, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 255, width: 45, color: '#E56666', value: 100, label: "80"},
      {pos: 310, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 325, width: 45, color: '#E56666', value: 100, label: "80"},
      {pos: 385, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 400, width: 45, color: '#E56666', value: 100, label: "80"},
      {pos: 455, width: 45, color: '#6C47A7', value: 200, label: "70"},
      {pos: 470, width: 45, color: '#E56666', value: 100, label: "80"}
    ],
    xAxis: {
      length: 1093,
      "stroke-width": 2,
      color: '#E6E2DF',
      labelsType: 'custom_bubbles',
      labels: [
        {pos: 60, text: 'S', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 130, text: 'M', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 200, text: 'T', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 270, text: 'W', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 340, text: 'T', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 415, text: 'F', type: 'bubble', "font-size": 20, "font-family": 'Verdana'},
        {pos: 485, text: 'S', type: 'bubble', "font-size": 20, "font-family": 'Verdana'}
      ]
    },
    yAxis: {
      length: 423,
      "stroke-width": 0,
      name: 'hs',
      labels: [
        {pos: 60, text: '2\navg', width: 1090, type: 'dotted', "stroke-width": 3, color: '#6C53C3', "text-color": "#6C53C3", "font-size": 13},
        {pos: 150, text: '4.3\navg', width: 1090, type: 'dotted', "stroke-width": 3, color: '#F0ACAC', "text-color": "#F0ACAC", "font-size": 13},
        {pos: 30, text: '1', width: 1090, type: 'dotted', "stroke-width": 3, color: '#E6E2DF', "text-color": "#ADB6BF"},
        {pos: 120, text: '3', width: 1090, type: 'dotted', "stroke-width": 3, color: '#E6E2DF', "text-color": "#ADB6BF"},
        {pos: 220, text: '5', width: 1090, type: 'dotted', "stroke-width": 3, color: '#E6E2DF', "text-color": "#ADB6BF"},
        {pos: 320, text: '7', width: 1090, type: 'dotted', "stroke-width": 3, color: '#E6E2DF', "text-color": "#ADB6BF"}
      ]
    },
    centerx: 10,
    centery: 370,
    canvasSize: [530,400]
  }
  doubleAxisBars4 = new EdBarChart(r_7_2, doubleAxisParams4);
  doubleAxisBars4.draw();
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