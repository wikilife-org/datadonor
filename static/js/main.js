var pieChart;
var animatedPie;
var doubleAxisBars;
var animatedQuarterPie;
var doubleAxisParams;

function drawSocialGraph(elments1, elements2){
	  var r_1_1 = Raphael('canvas_1_1', 420, 420);
	  animatedPie = new EdAnimatedPie(r_1_1, elments1, {
	    animationTime: 900,
	    easing: '<',
	    useAnimationDelay: false,
	    lineWidth: 70,
	    fontSize: 20,
	    centerx: 210,
	    centery: 210,
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
	      x: 180,
	      y: 170,
	      path: '/static/img/iconos/overall_avg.png'
	    }
	  });
	  animatedPie.draw();

	  
	  var r_1_2 = Raphael('canvas_1_2', 420, 420);
	  animatedPie2 = new EdAnimatedPie(r_1_2, elements2, {
	    animationTime: 900,
	    easing: '<',
	    useAnimationDelay: false,
	    lineWidth: 70,
	    fontSize: 20,
	    centerx: 210,
	    centery: 210,
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
	      x: 177,
	      y: 170,
	      path: '/static/img/iconos/your_avg.png'
	    }
	  });
	  animatedPie2.draw();
}

function drawShareGraphs(data){
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
  $('#data_2_1 .global_data').html(data.global_data.facebook.posts);
  $('#data_2_1 .user_data').html(data.user_data.facebook.posts);
  
  dotChart = new EdDotChart(r_2_1, elements1, graphConfig);
  dotChart.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([data.global_data.twitter.tweets, data.user_data.twitter.tweets], maxPercentage, 100);
  var r_2_2 = Raphael('canvas_2_2', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_2_2 .global_data').html(data.global_data.twitter.tweets);
  $('#data_2_2 .user_data').html(data.user_data.twitter.tweets);

  dotChart2 = new EdDotChart(r_2_2, elements1, graphConfig);
  dotChart2.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([data.global_data.facebook.likes, data.user_data.facebook.likes], maxPercentage, 100);
  var r_2_3 = Raphael('canvas_2_3', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_2_3 .global_data').html(data.global_data.facebook.likes);
  $('#data_2_3 .user_data').html(data.user_data.facebook.likes);

  dotChart3 = new EdDotChart(r_2_3, elements1, graphConfig);
  dotChart3.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([data.global_data.twitter.retweets, data.user_data.twitter.retweets], maxPercentage, 100);
  var r_2_4 = Raphael('canvas_2_4', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_2_4 .global_data').html(data.global_data.twitter.retweets);
  $('#data_2_4 .user_data').html(data.user_data.twitter.retweets);

  dotChart4 = new EdDotChart(r_2_4, elements1, graphConfig);
  dotChart4.draw();
}

function drawEducationGraph(data){
  var adapter = new EducationAdapter();
  var elements = adapter.getParameters(data);
  console.log('QUARTER PIE ADAPTER');
  console.log(elements);
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
  
  for(var i in elements){
      $('li[ref='+i+'] span.perc_number').html(elements[i].percentage);
      $('li[ref='+i+'] a span').html(elements[i].text);
      if(elements[i].selected){ 
        $('li[ref='+i+']').addClass('active');
        $('.hat_bottom').addClass('red');
      }
  }
}

function drawWorkGraph(data){
  var adapter = new WorkAdapter();
  var result = adapter.getParameters(data, 423, 80);
  var r_4_1 = Raphael('canvas_4_1', 1093, 423);
  doubleAxisParams = {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: true,
    drawLabels: true,
    elements: result.elements,
    xAxis: {
      length: 1093,
      "stroke-width": 2,
      color: '#F1F2F2',
      labels: []
    },
    yAxis: {
      length: 423,
      "stroke-width": 0,
      name: 'years',
      labels: result.yLabels
    },
    centerx: 30,
    centery: 400,
    canvasSize: [1093,425]
  }
  doubleAxisBars = new EdBarChart(r_4_1, doubleAxisParams);
  doubleAxisBars.draw();
}

function drawExerciseGraphs(data){
  console.log(data);
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
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([parseInt(data.running.global_data), parseInt(data.running.user_data)], maxPercentage, 100);
  var r_5_1 = Raphael('canvas_5_1', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_5_1 .global_data').html(data.running.global_data);
  $('#data_5_1 .user_data').html(data.running.user_data); 
  var dotChart = new EdDotChart(r_5_1, elements1, graphConfig);
  dotChart.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([parseInt(data.walking.global_data), parseInt(data.walking.user_data)], maxPercentage, 100);
  var r_5_2 = Raphael('canvas_5_2', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_5_2 .global_data').html(data.walking.global_data);
  $('#data_5_2 .user_data').html(data.walking.user_data); 
  var dotChart = new EdDotChart(r_5_2, elements1, graphConfig);
  dotChart.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([parseInt(data.elliptical.global_data), parseInt(data.elliptical.user_data)], maxPercentage, 100);
  var r_5_3 = Raphael('canvas_5_3', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_5_3 .global_data').html(data.elliptical.global_data);
  $('#data_5_3 .user_data').html(data.elliptical.user_data); 
  var dotChart = new EdDotChart(r_5_3, elements1, graphConfig);
  dotChart.draw();
  
  
}

function drawStepsGraph(data){
  var adapter = new StepsAdapter();
  var result = adapter.getParameters(data, 400, 20000);
  //console.log(result);
  var r_6_1 = Raphael('canvas_6_1', 1093, 423);
  doubleAxisParams2 = {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: true,
    drawLabels: true,
    elements: result.elements,
    xAxis: {
      length: 1093,
      "stroke-width": 2,
      color: '#F1F2F2',
      labelsType: 'custom_bubbles',
      name: 'Day',
      labels: result.xLabels
    },
    yAxis: {
      length: 423,
      "stroke-width": 0,
      name: 'Steps',
      labels: result.yLabels
    },
    centerx: 30,
    centery: 400,
    canvasSize: [1093,425]
  }
  doubleAxisBars2 = new EdBarChart(r_6_1, doubleAxisParams2);
  doubleAxisBars2.draw();
}

function drawMilesGraph(data){
  var adapter = new MilesAdapter();
  var result = adapter.getParameters(data, 400, 60,[10,20,30,40]);
  var r_7_1 = Raphael('canvas_7_1', 530, 400);
  doubleAxisParams3 = {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: true,
    drawLabels: true,
    elements: result.elements,
    xAxis: {
      length: 1093,
      "stroke-width": 2,
      color: '#E6E2DF',
      labelsType: 'custom_bubbles',
      labels: result.xLabels
    },
    yAxis: {
      length: 423,
      "stroke-width": 0,
      name: 'miles',
      labels: result.yLabels
    },
    centerx: 10,
    centery: 370,
    canvasSize: [530,400]
  }
  doubleAxisBars3 = new EdBarChart(r_7_1, doubleAxisParams3);
  doubleAxisBars3.draw();
  
  $('#data_7_1 .left .number_stat h2').html(data.global_avg);
  $('#data_7_1 .right .number_stat h2').html(data.user_avg);
}

function drawHoursGraph(data){
  var adapter = new MilesAdapter();
  var result = adapter.getParameters(data, 400, 9,[1,3,4,7]);
  var r_7_2 = Raphael('canvas_7_2', 530, 400);
  doubleAxisParams4 = {
    axis: 'both',
    barsAxis: 'x',
    drawAxis: true,
    drawLabels: true,
    elements: result.elements,
    xAxis: {
      length: 1093,
      "stroke-width": 2,
      color: '#E6E2DF',
      labelsType: 'custom_bubbles',
      labels: result.xLabels
    },
    yAxis: {
      length: 423,
      "stroke-width": 0,
      name: 'hs',
      labels: result.yLabels
    },
    centerx: 10,
    centery: 370,
    canvasSize: [530,400]
  }
  doubleAxisBars4 = new EdBarChart(r_7_2, doubleAxisParams4);
  doubleAxisBars4.draw();
  
  $('#data_7_2 .left .number_stat h2').html(data.global_avg);
  $('#data_7_2 .right .number_stat h2').html(data.user_avg);
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
  
  $.getJSON( "../../static/js/adapter/examples/education", function( data ) {
    drawEducationGraph(data);
  });
  
  $.getJSON( "../../static/js/adapter/examples/work", function( data ) {
    console.log('WORK!!!!');
    drawWorkGraph(data);
  });
  
  $.getJSON( "../../static/js/adapter/examples/exercise", function( data ) {
    drawExerciseGraphs(data);
  });
  
  $.getJSON( "../../static/js/adapter/examples/steps", function( data ) {
    //console.log('STEPS!');
    drawStepsGraph(data);
  });
  
  $.getJSON( "../../static/js/adapter/examples/miles", function( data ) {
    //console.log('MILES!');
    drawMilesGraph(data);
  });
  
  $.getJSON( "../../static/js/adapter/examples/hours", function( data ) {
    console.log('HOURS!');
    drawHoursGraph(data);
  });
  
};

$(document).ready(function(){
  $('#your_lvl_c li').click(function (event) {
    var pos = $(this).attr('ref');
    //line = animatedQuarterPie.lines[pos];
    for(var i in animatedQuarterPie.lines){
      line = animatedQuarterPie.lines[i];
      if(pos == i){
        line.animate({"stroke": '#E56666'}, 500);
      }else{
        //line.animate({"stroke": animatedQuarterPie.colors[i]}, 500);
        line.animate({"stroke": '#7737c7'}, 500);
      }
    }
    
    $.ajax({
      dataType: "json",
      type: "POST",
      url: "../../static/js/adapter/examples/education_post",
      data: { education_level: animatedQuarterPie.elements[pos].server_key },
      success: function(data){
        drawEducationGraph(data);
      }
    });
    
  });
  
  $('#age_select_form').submit(function(){
    console.log('form submitted!');
    var age = $('#age_select_value').val();
    $('#canvas_4_1').html('');
    $.ajax({
      dataType: "json",
      type: "POST",
      url: "../../static/js/adapter/examples/work_post",
      data: { working_experience: age },
      success: function(data){
        drawWorkGraph(data);
      }
    });
    return false;
  });
});