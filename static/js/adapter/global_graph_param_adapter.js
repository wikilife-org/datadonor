StepsAdapter = function(){

  this.getParameters = function(json, totalHeight, maxValue){

    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};

    var ordered = [];
    ordered.push([json.days.sunday,'Sunday']);
    ordered.push([json.days.monday,'Monday']);
    ordered.push([json.days.tuesday,'Tuesday']);
    ordered.push([json.days.wednesday,'Wednesday']);
    ordered.push([json.days.thursday,'Thursday']);
    ordered.push([json.days.friday,'Friday']);
    ordered.push([json.days.saturday,'Saturday']);

    elements = this.addElements(ordered, totalHeight, maxValue);
    yLabels = this.getYLabels(ordered, json, totalHeight, maxValue);
    xLabels = this.getXLabels(ordered);

    result.elements = elements;
    result.yLabels = yLabels;
    result.xLabels = xLabels;

    return result;
  }

  this.getValueHeight = function(value, totalHeight, maxValue){
    //console.log('VALUE: '+value);
    //console.log('TOTAL: '+totalHeight);
    //console.log('maxValue: '+maxValue);
    var valuePercentage = (value*100)/maxValue;
    var valueHeight = (valuePercentage*totalHeight)/100;
    return valueHeight;
  }

  this.addElements = function(json, totalHeight, maxValue){
    var currentPos = 70;
    var globalColor = '#7737c7';
    var userColor = '#E56666';
    var elements = [];

    //for(var i = 0; i < json.data.length; i = i+2){
    for(var i in json){
      var item = {
        pos: currentPos,
        color: globalColor,
        width: 62,
        label: json[i],
        vlabel: json[i],
        value: this.getValueHeight(json[i], totalHeight, maxValue),
      }



      elements.push(item);

      currentPos = currentPos + 144;
    }

    return elements;
  }

  this.getYLabels = function(json, orig_json, totalHeight, maxValue){
    var labels = [];
    //var step = Math.ceil((maxValue/totalHeight))*100;

    var currentY = 1000;

    var gloabalAvgLabel = {
      pos: this.getValueHeight(orig_json.avg, totalHeight, maxValue),
      //text: orig_json.global_avg_steps.toString()+'\navg',
      text: orig_json.avg.toString(),
      width: 1090,
      type: 'dotted',
      "stroke-width": 3,
      color: '#7737c7',
      "text-color": "#7737c7",
      is_avg: true
    }
    labels.push(gloabalAvgLabel);



    //for(var i = 0; i < 6; i++){
    while(currentY <= maxValue){
      var label = {
        pos: this.getValueHeight(currentY, totalHeight, maxValue),
        //text: currentY.toString(),
        text: '',
        width: 1090,
        type: 'dotted',
        "stroke-width": 3,
        color: '#F1F2F2',
        "text-color": "#ADB6BF"
      }

      labels.push(label);
      currentY = currentY + 1000;
    }



    return labels;
  }

  this.getXLabels = function(json){
    xLabels = [];
    currentPos = 132;
    for(var i in json){
      var label = {pos: currentPos, text: json[i][1][0].toUpperCase(), type: 'bubble', "font-size": 20, "font-family": 'Gotham-Ultra'};
      xLabels.push(label);
      currentPos = currentPos + 144;
    }
    return xLabels;
  }
}