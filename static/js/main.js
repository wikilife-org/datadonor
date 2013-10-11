var pieChart;
var animatedPie;
var doubleAxisBars;
var animatedQuarterPie;
var doubleAxisParams;
var SingleBarChart;
_api_env = 'hard';

function workCallback(args){
  //$('#age_input li a[data-key=15-25]');
  console.log(args);
  $('#age_input li a[data-key='+args[0]+']').click();
}

function drawSocialGraph(json){
  console.log(json);
  var global_data = json.global_data;
  $('.block.twitter ul li span.global_data').html(pad(global_data.twitter.count, 2));
  $('.block.facebook ul li span.global_data').html(pad(global_data.facebook.count, 2));
  $('.block.google_plus ul li span.global_data').html(pad(global_data.gmail.count, 2));
  $('.block.linkedin ul li span.global_data').html(pad(global_data.linkedin.count, 2));
  $('.block.foursquare ul li span.global_data').html(pad(global_data.foursquare.count, 2));
  
  var user_data = json.user_data;
  $('.block.twitter ul li span.user_data').html(pad(user_data.twitter.count, 2));
  $('.block.facebook ul li span.user_data').html(pad(user_data.facebook.count, 2));
  $('.block.google_plus ul li span.user_data').html(pad(user_data.gmail.count, 2));
  $('.block.linkedin ul li span.user_data').html(pad(user_data.linkedin.count, 2));
  $('.block.foursquare ul li span.user_data').html(pad(user_data.foursquare.count, 2));
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
  $('#data_2_1 .global_data').html(pad(data.global_data.facebook.posts,2));
  $('#data_2_1 .user_data').html(pad(data.user_data.facebook.posts,2));
  
  dotChart = new EdDotChart(r_2_1, elements1, graphConfig);
  dotChart.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([data.global_data.twitter.tweets, data.user_data.twitter.tweets], maxPercentage, 100);
  var r_2_2 = Raphael('canvas_2_2', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_2_2 .global_data').html(pad(data.global_data.twitter.tweets,2));
  $('#data_2_2 .user_data').html(pad(data.user_data.twitter.tweets,2));

  dotChart2 = new EdDotChart(r_2_2, elements1, graphConfig);
  dotChart2.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([data.global_data.facebook.likes, data.user_data.facebook.likes], maxPercentage, 100);
  var r_2_3 = Raphael('canvas_2_3', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_2_3 .global_data').html(pad(data.global_data.facebook.likes,2));
  $('#data_2_3 .user_data').html(pad(data.user_data.facebook.likes,2));

  dotChart3 = new EdDotChart(r_2_3, elements1, graphConfig);
  dotChart3.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([data.global_data.twitter.retweets, data.user_data.twitter.retweets], maxPercentage, 100);
  var r_2_4 = Raphael('canvas_2_4', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_2_4 .global_data').html(pad(data.global_data.twitter.retweets,2));
  $('#data_2_4 .user_data').html(pad(data.user_data.twitter.retweets,2));

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
  console.log('PRE PARAMS WORK');
  var adapter = new WorkAdapter();
  var result = adapter.getParameters(data, 423, 80, workCallback);
  console.log('POST PARAMS WORK');
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
      display: true,
      radius: 100,
      color: '#B3B3B3'
    }
  };
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([parseInt(data[0].global_times), parseInt(data[0].user_times)], maxPercentage, 100);
  var r_5_1 = Raphael('canvas_5_1', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_5_1 .global_data').html(pad(data[0].global_times,2));
  $('#data_5_1 .user_data').html(pad(data[0].user_times,2)); 
  var dotChart = new EdDotChart(r_5_1, elements1, graphConfig);
  dotChart.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([parseInt(data[1].global_times), parseInt(data[1].user_times)], maxPercentage, 100);
  var r_5_2 = Raphael('canvas_5_2', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_5_2 .global_data').html(pad(data[1].global_times,2));
  $('#data_5_2 .user_data').html(pad(data[1].user_times,2)); 
  var dotChart = new EdDotChart(r_5_2, elements1, graphConfig);
  dotChart.draw();
  
  var maxPercentage = 100;
  var elements1 = adapter.getParameters([parseInt(data[2].global_times), parseInt(data[2].user_times)], maxPercentage, 100);
  var r_5_3 = Raphael('canvas_5_3', 210, 210);
  if(maxPercentage < 100) graphConfig.perimeter.display = true;
  $('#data_5_3 .global_data').html(pad(data[2].global_times,2));
  $('#data_5_3 .user_data').html(pad(data[2].user_times,2)); 
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
  
  $('#data_6_1 .bloq.right .number_stat h2').html(pad(data.global_avg_steps,2));
  $('#data_6_1 .bloq.left .number_stat h2').html(pad(data.user_avg_steps,2));
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
  
  $('#data_7_1 .left .number_stat h2').html(pad(data.global_avg_miles));
  $('#data_7_1 .right .number_stat h2').html(pad(data.user_avg_miles));
}

function drawHoursGraph(data){
  var adapter = new HoursAdapter();
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
  
  $('#data_7_2 .left .number_stat h2').html(pad(data.global_avg_hours,2));
  $('#data_7_2 .right .number_stat h2').html(pad(data.user_avg_hours,2));
}

function drawNutrientProportionGraph(data){

  var r_9_1 = Raphael('canvas_9_1', 1095, 115);
  var adapter = new NutrientsAdapter();
  var elems = adapter.getParameters(data.global_data,['#B48AEA','#8A45E5','#7737C7','#3E3EA5',]);
  SingleBarChart = new EdSingleBarChart(r_9_1, elems, {
    x: 20,
    y: 5,
    width: 1050,
    height: 83,
    fontSize: 47,
    fontColor: '#ffffff',
    first_icon: '/static/img/step_9/ico_1.png',
    end_icon: '/static/img/step_9/porcentaje.png'
  });
  SingleBarChart.draw();
  
  var r_9_2 = Raphael('canvas_9_2', 1095, 115);
  var adapter = new NutrientsAdapter();
  var elems = adapter.getParameters(data.global_data,['#FF9C8C','#FF836F','#E56666','#D44B5F',]);
  SingleBarChart = new EdSingleBarChart(r_9_2, elems, {
    x: 20,
    y: 5,
    width: 1050,
    height: 83,
    fontSize: 47,
    fontColor: '#ffffff',
    first_icon: '/static/img/step_9/ico_2.png',
    end_icon: '/static/img/step_9/porcentaje.png'
  });
  SingleBarChart.draw();

}

function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

window.onload = function () {
  
  /*********** PIE CHARTS *******************/
  $.getJSON( _api_urls[_api_env].social_reach, function( data ) {
    //console.log(data);
    drawSocialGraph(data);
  });
  
  $.getJSON( _api_urls[_api_env].share, function( data ) {
    drawShareGraphs(data);
  });
  
  $.getJSON( _api_urls[_api_env].education, function( data ) {
    drawEducationGraph(data);
  });
  
  $.getJSON( _api_urls[_api_env].work, function( data ) {
    //console.log('WORK!!!!');
    drawWorkGraph(data);
  });
  
  $.getJSON( _api_urls[_api_env].exercise, function( data ) {
    drawExerciseGraphs(data);
  });
  
  $.getJSON( _api_urls[_api_env].steps, function( data ) {
    //console.log('STEPS!');
    drawStepsGraph(data);
  });
  
  $.getJSON( _api_urls[_api_env].miles, function( data ) {
    //console.log('MILES!');
    drawMilesGraph(data);
  });
  
  $.getJSON( _api_urls[_api_env].hours, function( data ) {
    //console.log('HOURS!');
    drawHoursGraph(data);
  });
  
  $.getJSON( _api_urls[_api_env].nutrients, function( data ) {
    //console.log('NUTRIENT PROPORTION!');
    drawNutrientProportionGraph(data);
  });
  
  $.getJSON( _api_urls[_api_env].weight, function( data ) {
    console.log('WEIGHT!');
    $('.weight_values .man .value').html(data.global_data.men.value);
    $('.weight_values .woman .value').html(data.global_data.women.value);
    $('#weight_number').html(data.user_data.value);
  });
  
  $.getJSON( _api_urls[_api_env].height, function( data ) {
    console.log('WEIGHT!');
    $('.height_values .man .value').html(data.global_data.men.value);
    $('.height_values .woman .value').html(data.global_data.women.value);
    console.log('HEIGHT USER: '+data.user_data.value);
    $('#height_number').html(data.user_data.value);
  });
  
  $.getJSON( _api_urls[_api_env].bmi, function( data ) {
    console.log('WEIGHT!');
    $('.bmi_values .man .value').html(data.global_data.men.value);
    $('.bmi_values .woman .value').html(data.global_data.women.value);
    $('.your_bmi h2').html(data.user_data.value);
  });
  
  $.getJSON( _api_urls[_api_env].user_exercise, function( data ) {
    for(var i = 1; i <= data.length; i++){
      $($('.you_cards ul li')[i]).html('<p><span>'+data[i-1].title+'</span><br />'+data[i-1].message+'</p>');
    }
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
      url: _api_urls[_api_env].education_post,
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
      url: _api_urls[_api_env].work_post,
      data: { working_experience: age },
      success: function(data){
        drawWorkGraph(data);
      }
    });
    return false;
  });
  
  $("#weight_slider").on("slidestop", function(event, ui) {
    $.ajax({
      dataType: "json",
      type: "POST",
      url: _api_urls[_api_env].weight,
      data: { unit: 'Lbs', value: $("#weight_slider").slider("value") },
      success: function(data){
        
      }
    });
  });
  
  $("#height_slider").on("slidestop", function(event, ui) {
    $.ajax({
      dataType: "json",
      type: "POST",
      url: _api_urls[_api_env].height,
      data: { unit: 'Ft', value: $("#height_slider").slider("value") },
      success: function(data){
        
      }
    });
  });
});