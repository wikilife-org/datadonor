$( document ).ready (

	function ( )
	{		
		
		$( "#reset" ).click (
				
				function ( event )
				{  
					$("li").removeClass("ui-selected");
					$("a").removeClass("selected");
					
				}
			);
		
		$( ".gender" ).click (
		
			function ( event )
			{
				event.preventDefault ( );
				
				if( $( this ).hasClass( 'selected' ) )
				{
					$( this ).removeClass( 'selected' );	
				}
				else
				{
					$( this ).addClass( 'selected' );	
				}
				
			}
		);
		
		$( ".column-left .select" ).click (
		
			function ( event )
			{
				event.preventDefault ( );
				
				
				if(  $( this ).parent( ).hasClass( 'open-box' ) )
				{
					$( '.open-box' ).find( '.selectable' ).slideToggle('slow');
					
					$( '.open-box' ).removeClass( 'open-box' );
				}else
				{
					$( '.open-box' ).find( '.selectable' ).slideToggle('slow');

					$( '.open-box' ).removeClass( 'open-box' );
	
					$( this ).parent( ).addClass( 'open-box' );
	
					$( this ).parent( ).find( '.selectable' ).slideToggle('slow');
				}
			}
		);
		
		$( ".variable-component .select" ).click (
		
			function ( event )
			{
				event.preventDefault ( );
			
				$( this ).parent( ).find( '.selectable' ).slideToggle('slow');
	
			}
		);
		
		$( ".variable-component .selectable li" ).selectable(
		{
			start: function( event, ui ) 
			{
				$( this ).parent( ).find( '.ui-selecting').removeClass( 'ui-selecting' )
			},
			stop: function( event, ui ) 
				{
					
					$( this ).parent( ) .parent( ).find( '.select' ).html( $( this ).html() )
					$( this ).parent( ) .parent( ).find( '.selectable' ).slideToggle('slow');
				}
		
		});
		
		$( ".selectable li" ).click (
		
			function ( event )
			{
				event.preventDefault ( );
				
				$( this ).parent( ).find( '.selectable' ).slideToggle('slow');
				
			}
		);
		
		

	}
	
);

google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(init);

function init(){
	
	$( "#submit" ).click (
			
			function ( event )
			{$("body").addClass("loading"); 
				event.preventDefault ( );
				service_url = getStat();
				draw(service_url);
				
			}
		);
	
	return false;
	
}

function getStat(){
	var selected_ages = [];
	$('#age-box ul').children('.ui-selected').each(function(){
		selected_ages.push( $(this).attr('id'));
    });

	var selected_sleep = [];
	$('#sleep-box ul').children('.ui-selected').each(function(){
		selected_sleep.push( $(this).attr('id'));
    });

	var selected_height = [];
	$('#Height-box ul').children('.ui-selected').each(function(){
		selected_height.push( $(this).attr('id'));
    });

	var selected_weight= [];
	$('#weight-box ul').children('.ui-selected').each(function(){
		selected_weight.push( $(this).attr('id'));
    });
	
	var selected_running = [];
	$('#running-box ul').children('.ui-selected').each(function(){
		selected_running.push( $(this).attr('id'));
    });
	
	var selected_mood = [];
	$('#mood-box ul').children('.ui-selected').each(function(){
		selected_mood.push( $(this).attr('id'));
    });
	
	var selected_headache = [];
	$('#headache-box ul').children('.ui-selected').each(function(){
		selected_headache.push( $(this).attr('id'));
    });
	
	var selected_location = [];
	$('#location-box ul').children('.ui-selected').each(function(){
		selected_location.push( $(this).attr('id'));
    });
	
	var selected_living = [];
	$('#living-box ul').children('.ui-selected').each(function(){
		selected_living.push( $(this).attr('id'));
    });

	var selected_gender = [];
	$( '#gender-box' ).find( '.selected').each(function(){
		selected_gender.push( $(this).attr('id'));
    });

	var selected_variable = [];
	var units = [];
	var names = [];
	$('#vairable-select ul').children('.ui-selecting').each(function(){
		selected_variable.push( $(this).attr('id'));
		units.push( $(this).attr('unit'));
		names.push($(this).text());
    });
	
	factors = "&age="+selected_ages.join(",")+
	"&gender="+selected_gender.join(",")+
	"&location="+selected_location.join(",")+
	"&sleep="+selected_sleep.join(",")+
	"&height="+selected_height.join(",")+
	"&weight="+selected_weight.join(",")+
	"&livingwith="+selected_living.join(",")+
	"&running="+selected_running.join(",")+
	"&mood="+selected_mood.join(",")+
	"&headache="+selected_headache.join(","); 
	
	propId = selected_variable.join(",")
	unit = units.join(",")
	name = names.join(",");
	
	from_date = $("#from").datepicker( 'getDate' );
	day1 = from_date.getDate();
	month1 = from_date.getMonth() + 1;
	if (month1 < 10){
		month1 = "0" + month1;
	}
	year1 = from_date.getFullYear();
	var fullDate1 = year1 + "-" + month1 + "-" + day1;
	to_date = $("#to").datepicker( 'getDate' );
	day2 = to_date.getDate();
	month2 = to_date.getMonth() + 1;

	if (month2 < 10){
		month2 = "0" + month2;
	}
	year2 = to_date.getFullYear();
	var fullDate2 = year2 + "-" + month2 + "-" + day2;

	var today = new Date();
	var dd = today.getDate() + 7;
	var mm = today.getMonth()+1; //January is 0!
	if (mm < 10){
		mm = "0" + mm;
	}
	var yyyy = today.getFullYear();
	var fullDateToday = yyyy + "-" + mm + "-" + dd;
	
	if (fullDate1 == fullDateToday && fullDate2 == fullDateToday){
		fullDate1 = "";
		fullDate2 = "";
	}
	
	serviceUrl = "http://api.wikilife.org/3/stats/aggregation?value_id="+propId+"&summary_id=0"+factors+"&from=" + fullDate1  + "&to=" + fullDate2;
	a = new Object();
	a["url"] = serviceUrl;
	a["unit"] = unit;
	a["name"] = name;
	return a;
}

function draw(obj){
	
	 $.getJSON(obj["url"], function(resultados) {

		  var data_avg = new google.visualization.DataTable();
		  var data_count = new google.visualization.DataTable();
		  var data_sum = new google.visualization.DataTable();
		  
		  data_avg.addColumn('string', 'Date');
		  data_count.addColumn('string', 'Date');
		  data_sum.addColumn('string', 'Date');
		  
		  var factors = new Object();
		  factors[0] = "Gender";
		  factors[1] = "Age";
		  factors[2] = "Height";
		  factors[3] = "Weight";
		  factors[4] = "BMI";
		  factors[5] = "Location";
		  factors[6] = "Living With";
		  factors[7] = "Sleep";
		  factors[8] = "Running";
		  factors[9] = "Mood";
		  factors[10] = "Sex";
		  factors[11] = "Headache";
		  factors[12] = "Smoking";
		  

		  $.each(resultados, function(index, resultado) {
			  var n = unescape(resultado.desc);
			  n = n.replace(/\\/g, "");
			  
			  var desc = n.substring(n.indexOf("__")+2, n.length)
			  var n=desc.split("/");
			  
			  h = [];
			  k = [];
			  k[0] = obj["name"];
			  for (var i=0;i<n.length;i++){
				  r = []
				  a = n[i]
				  if (a != ".*"){
					  var g = a.split(",");
					  for (var j=0;j<g.length;j++){
						  value = document.getElementById(g[j]).innerHTML;
						  r.push(value);
					  }
					  k.push(factors[i]);
					  h.push(factors[i] + ": "+r.join(", ") );
				  }
			  }
			  
			  console.log(h);
			  console.log(h.length);
			  if (h.length > 0){
				  d = h.join(" | ");}
			  else{
				  d= "All";
			  }
			  o = k.join(", ");
			  data_avg.addColumn('number', d);
			  data_count.addColumn('number', d);
			  data_sum.addColumn('number', d);


		  });
		 
		  items_avg = [];
		  items_count = [];
		  items_sum = [];
		  
		  var avg_list = new Object();
		  var count_list = new Object();
		  var sum_list = new Object();
		  
		  
			  var init_list = []
			  for (var i=0;i<resultados.length;i++)
			  { 
				  init_list[0] = 0;
				  init_list[i+1] = 0;
				  
			  }
			  for (var i=0;i<resultados.length;i++)
			  { 
				  resultado = resultados[i];
				  for (var j=0;j<resultado.data.length;j++) {
					  var val = resultado.data[j];

					  if (!avg_list[val.date]){
						  avg_list[val.date] = init_list.slice(0);
						  avg_list[val.date][0] = val.date
						  }
					  if (!count_list[val.date]){
						  count_list[val.date] = init_list.slice(0);
						  count_list[val.date][0] = val.date
						  }
					  if (!sum_list[val.date]){
						  sum_list[val.date] = init_list.slice(0);
						  sum_list[val.date][0] = val.date
						  }
					  avg_list[val.date][i+1] = parseFloat(val.avg.toFixed(2));
					  count_list[val.date][i+1] = parseFloat(val.count.toFixed(2));
					  sum_list[val.date][i+1] = parseFloat(val.sum.toFixed(2));

				  };
			  };

			  $.each(avg_list, function(key, val) {
				  items_avg.push(val);
			  });
			  $.each(count_list, function(key, val) {
				  items_count.push(val);
			  });
			  $.each(sum_list, function(key, val) {
				  items_sum.push(val);
			  });
			  
			  data_avg.addRows(items_avg);
			  data_count.addRows(items_count);
			  data_sum.addRows(items_sum);
			  
			var options1 = {
					  
					   backgroundColor: '#EFEFEF',
					   width: 340,
						height: 340,
						//legend: {position: 'in', textStyle: {color: 'black', fontSize: 12}},
						vAxis: {format:'#,# '+obj["unit"]},
					
					};
			
		    var chart1 = new google.visualization.LineChart(document.getElementById('firs-graph'));
		    chart1.draw(data_avg, options1);
		    $("#comment1").html ("<h3>Wikilife Aggregation System - AVG.</h3><h4>Data generated from: <span>"+ o +"</span></h4>");
			    
		
		    var options2 = {
					  
					backgroundColor: '#EFEFEF',
					width: 640,
					height: 340,
					vAxis: {format:'#,# logs'},
					
					};
			
		    var chart2 = new google.visualization.LineChart(document.getElementById('second-graph'));
		    chart2.draw(data_count, options2);		
		    $("#comment2").html ("<h3>Wikilife Aggregation System - Count</h3><h4>Data generated from: <span>"+ o +"</span></h4>");
			    
			var options3 = {
					  
					   backgroundColor: '#EFEFEF',
					   width: 640,
					height: 340,
					vAxis: {format:'#,# '+obj["unit"]},
					hAxis: {format:'MMM d, y'},
					
					};
			
		    var chart3 = new google.visualization.LineChart(document.getElementById('third-graph'));
		    chart3.draw(data_sum, options3);	
		    $("#comment3").html ("<h3>Wikilife Aggregation System - Sum</h3><h4>Data generated from: <span>"+ o +"</span></h4>");
		    $("body").removeClass("loading"); 	
	 });
	
	
};

$( function ( ) {
 
	var prev = -1; // here we will store index of previous selection
	
	$('.selectable').selectable(
	{
    	selecting: function(e, ui) { // on select
        var curr = $(ui.selecting.tagName, e.target).index(ui.selecting); // get selecting item index
			if( e.shiftKey && prev > -1 )
			{ // if shift key was pressed and there is previous - select them all
				$(ui.selecting.tagName, e.target).slice(Math.min(prev, curr), 1 + Math.max(prev, curr)).addClass('ui-selected');
				prev = -1; // and reset prev
			} 
			else 
			{
				prev = curr; // othervise just save prev
			}
    }
	
	});

	$( "#from" ).datepicker (
	{
		defaultDate: "+1w",
		changeMonth: true,
		numberOfMonths: 3,
		dateFormat: "yy-mm-dd",
		onClose: function( selectedDate ) 
		{
			$( "#to" ).datepicker( "option", "minDate", selectedDate );
		}
	});
	
	$( "#to" ).datepicker ( 
	{
	  defaultDate: "+1w",
	  changeMonth: true,
	  numberOfMonths: 3,
	  dateFormat: "yy-mm-dd",
	  onClose: function( selectedDate ) 
		{
			$( "#from" ).datepicker( "option", "maxDate", selectedDate );
		}
	});
});
  


