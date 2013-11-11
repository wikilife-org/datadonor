if (typeof console == "undefined") var console = { log: function() {} };

$(document).ready(function () {
//READY START

	exploradorVersion();
	
	// SECTOR FIXED NAV
	if ($('.scroll_fixed_trigger').length) {
		$(window).scroll(function(){
		  
			  // PRINCIPAL CONTAINERS
			  var h = $('#container').height();
			  var y = $(window).scrollTop();
			 
			  // LEFT NAV FIXED
			  var fixedNav = $('.step_one').offset().top;
			  if( y > fixedNav ){
				$('.nav_steps').addClass('fixed');
			  } else {
			  	$('.nav_steps').removeClass('fixed');
			  }
			  // LEFT NAV FIXED
		  
		 });
	}
	// SECTOR FIXED NAV
	
	// NAVEGACION
	$('.nav_big_social a').live('click',function (event) {event.preventDefault();});
	// NAVEGACION
    
    // SECTOR FIXED NAV
	if ($('.maqueta_new').length) {
		var offsetOne = $('#step_one').offset().top - 150;
        var offsetfive = $('#step_five').offset().top - 150;
        var offseteight = $('#step_eight').offset().top - 150;
        var offseeleven = $('#step_eleven').offset().top - 150;
	}
	// SECTOR FIXED NAV
	
	// SCROLL SOLO
	$('.nav_steps a').click(function (event) {
		event.preventDefault();
		
		var idClick = $('#step_five').attr('data-scroll');
		
		if ($(this).hasClass('nav_one')) {
			$('body,html').animate({
				scrollTop: offsetOne
			}, 1000);
			return false;
		}
		
		if ($(this).hasClass('nav_two')) {
			$('body,html').animate({
				scrollTop: offsetfive
			}, 1000);
			return false;
		}
		
		if ($(this).hasClass('nav_three')) {
			$('body,html').animate({
				scrollTop: offseteight
			}, 1000);
			return false;
		}
		
		if ($(this).hasClass('nav_four')) {
			$('body,html').animate({
				scrollTop: offseeleven
			}, 1000);
			return false;
		}
			
	});
	// SCROLL SOLO
	
	// 3 STEP EFECTOS NAV
	$('#your_lvl_c li a').click(function (event) {
		event.preventDefault();
	
		if ($(this).parent().hasClass('active')) {
			$('#your_lvl_c li').removeClass('active');
			$('.hat_bottom').removeClass('red');
		} else {
			$('#your_lvl_c li a').parent().removeClass('active');
			$(this).parent().addClass('active');
			$('.hat_bottom').addClass('red');
		}
		
	});
	// 3 STEP EFECTOS NAV
	
	// AGE CHOSE INPUT
	$('#age_input li a').click(function (event) {
		event.preventDefault();
		
		
		if ($(this).parent().hasClass('active')) {
			$('#age_input li').removeClass('active');
			$('#age_select').removeClass('active');
		} else if ($(this).parent().hasClass('first')) {
			$('#age_input li a').parent().removeClass('active');
			$(this).parent().addClass('active');
			var leftContainer = $(this).parent().position().left - 10;
			$('#age_select').css({left: leftContainer+"px"});
			$('#age_select').addClass('active');
		} else {
			$('#age_input li a').parent().removeClass('active');
			$(this).parent().addClass('active');
			var leftContainer = $(this).parent().position().left - 5;
			$('#age_select').css({left: leftContainer+"px"});
			$('#age_select').addClass('active');
		}
			
	});
	// AGE CHOSE INPUT
	
	// SHARE SOCIAL
	$("#trigger_social").hover(
	  function () {
	  	$(this).stop(true,true);
	  	$(this).animate({height:"240px"},1000,'easeOutBounce');
	    $(this).addClass('active');
	  },
	  function () {
	  
	  	$(this).stop(true,true);
	   	$(this).animate({height:"59px"},300,function () {
	    $(this).removeClass('active');
	   	
	   	});
	  }
	);
	
	$("#trigger_social li").click(function (event) {
		event.preventDefault();
		if ($(this).hasClass('last')) {} else {
			var url = $(this).find('a').attr('href');
			window.open(url, '_blank');
		}
	});
	// SHARE SOCIAL
	
	// EMAIL SHARE POP-UP
	$('#email_trigger, .footer_social a.email').click(function (event) {
		event.preventDefault();
		$('#email_container').fadeIn();
	});
	$('#close_email').click(function (event) {
		event.preventDefault();
		$('#email_container').fadeOut();
	});
	// EMAIL SHARE POP-UP
	
	// SLIDER NUTRITION
	if ($('#weight_slider').length) {
		$('#weight_slider').slider({
		      range: 'min',
		      value: 112,
		      min: 0,
		      max: 200,
		      slide: function( event, ui ) {
		        var value = ui.value;
		        $('#weight_number').html(value);
		      }
		 });	
	}
	if ($('#height_slider').length) {
    var defheight = 5.8;
		$('#height_slider').slider({
		      range: 'min',
		      value: defheight.toFixed(1),
		      min: 0,
		      max: 8.5,
          step: 0.1,
		      slide: function( event, ui ) {
		        var value = ui.value.toFixed(1);
		        $('#height_number').html(value.replace('.', ','));
		      }
		 });	
	}
	// SLIDER NUTRITION
	
	
	// CARROUSELS NETWORKS

	// Activar navegacion
	
	$('.social_icons .boton.next').hide();
	
	var carOne = $('#carousel_one .overflow_icons ul').width();
	var carTwo = $('#carousel_two .overflow_icons ul').width();
	var carThree = $('#carousel_three .overflow_icons ul').width();
	var carFour = $('#carousel_four .overflow_icons ul').width();
	var carFive = $('#carousel_five .overflow_icons ul').width();
	
	if (carOne <= 930) {
		$('#carousel_one a.boton').hide();
	} 
	if (carTwo <= 930) {
		$('#carousel_two a.boton').hide();
	} 
	if (carThree <= 930) {
		$('#carousel_three a.boton').hide();
	} 
	if (carFour <= 930) {
		$('#carousel_four a.boton').hide();
	} 
	if (carFive <= 930) {
		$('#carousel_five a.boton').hide();
	} 
	
	// funciones que generan movimiento
	
	function $nextNetwork() {
		
		// Data slider
		var nu_pos = $(this).parent().find('.overflow_icons').attr('data-position');
		nu_pos--;
		
		// Overflow size
		var visibleArea = $(this).parent().find('.overflow_icons').width();
		var overflowWidth = $(this).parent().find('.overflow_icons').find('ul').width();
		var hiddenOverflow = overflowWidth - visibleArea;
		var leftMove = hiddenOverflow / 2;
		
		// Navegacion off
		var $prevCarousel = $(this).parent().find('.boton.prev');
		var $nextCarousel = $(this).parent().find('.boton.next');
		
		// Move element
		$nuevaPosicion = $(this).parent().find('.overflow_icons').find('ul');
		
		if (overflowWidth < visibleArea) {
			nu_pos = 0;
		} else if (nu_pos <= 0 ) {
			nu_pos = 0;
			$(this).parent().find('.overflow_icons').attr('data-position',0);
			$nuevaPosicion.stop(true,true);
			$nuevaPosicion.animate({left:'0px'},400);
			$nextCarousel.hide();
		} else {
			$nuevaPosicion.stop(true,true);
			$nuevaPosicion.animate({left:'-='+leftMove+'px'},400);
			$(this).parent().find('.overflow_icons').attr('data-position',nu_pos);
			$prevCarousel.show();
		}
		
	}
	
	function $prevNetwork() {
	
		// Data slider
		var nu_pos = $(this).parent().find('.overflow_icons').attr('data-position');
		nu_pos++;
		
		// Overflow size
		var visibleArea = $(this).parent().find('.overflow_icons').width();
		var overflowWidth = $(this).parent().find('.overflow_icons').find('ul').width();
		var hiddenOverflow = overflowWidth - visibleArea;
		var leftMove = hiddenOverflow / 2;
		
		// Navegacion off
		var $prevCarousel = $(this).parent().find('.boton.prev');
		var $nextCarousel = $(this).parent().find('.boton.next');
		
		// Move element
		$nuevaPosicion = $(this).parent().find('.overflow_icons').find('ul');
		
		if (overflowWidth < visibleArea) {
			nu_pos = 0;
		} else if (nu_pos >= 2 ) {
			nu_pos = 2;
			$(this).parent().find('.overflow_icons').attr('data-position',2);
			$nuevaPosicion.stop(true,true);
			$nuevaPosicion.animate({left: hiddenOverflow+'px'},400);
			$prevCarousel.hide();
		} else {
			$nuevaPosicion.stop(true,true);
			$nuevaPosicion.animate({left:'+='+leftMove+'px'},400);
			$(this).parent().find('.overflow_icons').attr('data-position',nu_pos);
			$nextCarousel.show();
		}
		
	}
	
	// MOVIMIENTO
	
	// EVENTO CLICK	
	
	$('.social_icons .boton').click(function (event) {event.preventDefault();})
	$('.social_icons .boton.next').click($nextNetwork);
	$('.social_icons .boton.prev').click($prevNetwork);
	
	// EVENTO CLICK
	
	// CARROUSELS NETWORKS
	
	
	// CLICK GRAFICO 11
//	$('#graphs_conditions .condition').click(function (event) {
//		event.preventDefault
//		$('#graphs_conditions .condition').removeClass('active');
//		$(this).addClass('active');
//	});
	
//	$('#graphs_conditions .done_condition').live('click',function (event) {
//		event.preventDefault();
//		
//		if ($(this).hasClass('next_subsector')) {
//			$(this).removeClass('next_subsector');
//			$(this).parent().parent().find('.graph_container').addClass('second_active');
//			$(this).find('span').hide().html('Done!').fadeIn(300);
//		} else if ($(this).parent().parent().find('.graph_container').hasClass('second_active')) {
//			$(this).addClass('next_subsector');
//			$('#graphs_conditions .condition').removeClass('active');
//			$('.graph_container').removeClass('second_active');
//			$(this).find('span').hide().html('Next').fadeIn(300);
//		} else {
//		  $('#graphs_conditions .condition').removeClass('active');
//		  $(this).find('span').hide().html('Next').fadeIn(300);
//		}
//		
//	});
	// CLICK GRAFICO 11
	
	// CLICK GRAFICO 12
	$('#select_complaints li').click(function (event) {
		event.preventDefault();
		$('#select_complaints li').removeClass('active');
		$(this).addClass('active');
	});
	
	// CLICK GRAFICO 12
	
	// CLICK GRAFICO 13
//	$('#chose_type li').click(function (event) {
//		event.preventDefault();
//		$('#chose_type li').removeClass('active');
//		$(this).addClass('active');
//	});
	// CLICK GRAFICO 13
	
	// CLICK GRAFICO 15
//	$('#graphs_emotions .condition').click(function (event) {
//		event.preventDefault
//		$('#graphs_emotions .condition').removeClass('active');
//		$(this).addClass('active');
//	});
//	
//	$('#graphs_emotions .done_condition').live('click',function (event) {
//		event.preventDefault();
//		
//		if ($(this).hasClass('next_subsector')) {
//			$(this).removeClass('next_subsector');
//			$(this).parent().parent().find('.graph_container').addClass('second_active');
//			$(this).find('span').hide().html('Done!').fadeIn(300);
//		} else if ($(this).parent().parent().find('.graph_container').hasClass('second_active')) {
//			$(this).addClass('next_subsector');
//			$('#graphs_emotions .condition').removeClass('active');
//			$('.graph_container').removeClass('second_active');
//			$(this).find('span').hide().html('Next').fadeIn(300);
//		} else {
//		    $('#graphs_emotions .condition').removeClass('active');
//		    $(this).find('span').hide().html('Next').fadeIn(300);
//		}
//	
//	});
	// CLICK GRAFICO 15
	
	// AUTOCOMPLETES TRIGGER
	//$('.select_stats').combobox();
	
	$('ul.ui-autocomplete').hover(
	  function() {
	    $('input.select_stats').addClass('on_ul');
	  }, function() {
	    $('input.select_stats').removeClass('on_ul');
	  }
	);
	// AUTOCOMPLETES TRIGGER
	
	// STEP 16
	
		$( "#mood_1 a" ).live('click',function (event) {event.preventDefault();});
		$( "#mood_2 a" ).live('click',function (event) {event.preventDefault();});
	
		// sliders your
		$( "#mood_1" ).slider({
		      range: 'min',
		      value: 1,
		      min: 0,
		      max: 10,
		      step:1,
			      slide: function( event, ui ) {
			        var value = ui.value;
			        $('#mood_1 .ui-slider-handle').html('<span>'+value+'</span>');
              
              if($('#mood_2').slider( "option", "value" ) == value){
                $('.mood_container').addClass('same_porcent');
              }else{
                $('.mood_container').removeClass('same_porcent')
              }
              
              if($('#mood_2').slider( "option", "value" ) < value){
               $('.mood_container .your_stats_mood ').css('z-index','1');
              }else{
                $('.mood_container .your_stats_mood ').css('z-index','2');
              }
              
			      }
		 });
		 //$('#mood_1 .ui-slider-handle').html('<span>1</span>');
		 
		 // sliders all
		 $( "#mood_2" ).slider({
		       range: 'min',
		       value: 5,
		       min: 0,
		       max: 10,
		       step:1,
		       disabled:true,
		 	      slide: function( event, ui ) {
		 	        var value = ui.value;
		 	        $('#mood_2 .ui-slider-handle').html('<span>'+value+'</span>');
		 	      }
		  });
		  //$('#mood_2 .ui-slider-handle').html('<span>5</span>');
		  
		   
		   // Cambia de valor en el click
		   $('#trigger_mood li a').click(function (event) {
		   		event.preventDefault();
//		   		var positionSlider = $(this).attr('data-valor');
//		   		$( "#mood_1" ).slider({value: positionSlider});
//		   		$('#mood_1 .ui-slider-handle').html('<span>'+positionSlider+'</span>');
		   });
	   
	   // STEP 16
	   
	   // TABS YOU REMOVE
	   $('.cards .you_cards ul li .close_tab').click(function (event) {
	   	event.preventDefault();
	   });
	   // TABS YOU REMOVE
	    
	
	//DORESIZE
	doResize();
	$(window).resize(function() {
		doResize();
	});

//READY OUT
});



//DORESIZE
function doResize(){
	
	var windowWidth = $(window).width();
	var windowHeight = $(window).height();
	
	//  NAV LEFT FIXED LANDSCAPE	
	if (windowWidth < 1280) {
		$('.nav_steps').css({left:"20px"});
		
	} else {
		var leftMargin = windowWidth - 1050;
		var distanciaNav = leftMargin/2;
		var margenFinal = distanciaNav - 100;
		$('.nav_steps').css({left: margenFinal+"px"});
	}
	//  NAV LEFT FIXED LANDSCAPE
	
	//  EMAIL SHARE
	$('#email_container').height(windowHeight);
	//  EMAIL SHARE	
	
}
//DORESIZE

//NAVEGADORES FIX
function exploradorVersion() {

	// NAVEGADOR FIX
	var BrowserDetect = {
	 init: function () {
	  this.browser = this.searchString(this.dataBrowser) || "An unknown browser";
	  this.version = this.searchVersion(navigator.userAgent)
	   || this.searchVersion(navigator.appVersion)
	   || "an unknown version";
	  this.OS = this.searchString(this.dataOS) || "an unknown OS";
	 },
	 searchString: function (data) {
	  for (var i=0;i<data.length;i++) {
	   var dataString = data[i].string;
	   var dataProp = data[i].prop;
	   this.versionSearchString = data[i].versionSearch || data[i].identity;
	   if (dataString) {
	    if (dataString.indexOf(data[i].subString) != -1)
	     return data[i].identity;
	   }
	   else if (dataProp)
	    return data[i].identity;
	  }
	 },
	 searchVersion: function (dataString) {
	  var index = dataString.indexOf(this.versionSearchString);
	  if (index == -1) return;
	  return parseFloat(dataString.substring(index+this.versionSearchString.length+1));
	 },
	 dataBrowser: [
	  {
	   string: navigator.userAgent,
	   subString: "Chrome",
	   identity: "Chrome"
	  },
	  {  string: navigator.userAgent,
	   subString: "OmniWeb",
	   versionSearch: "OmniWeb/",
	   identity: "OmniWeb"
	  },
	  {
	   string: navigator.vendor,
	   subString: "Apple",
	   identity: "Safari",
	   versionSearch: "Version"
	  },
	  {
	   prop: window.opera,
	   identity: "Opera",
	   versionSearch: "Version"
	  },
	  {
	   string: navigator.vendor,
	   subString: "iCab",
	   identity: "iCab"
	  },
	  {
	   string: navigator.vendor,
	   subString: "KDE",
	   identity: "Konqueror"
	  },
	  {
	   string: navigator.userAgent,
	   subString: "Firefox",
	   identity: "Firefox"
	  },
	  {
	   string: navigator.vendor,
	   subString: "Camino",
	   identity: "Camino"
	  },
	  {  // for newer Netscapes (6+)
	   string: navigator.userAgent,
	   subString: "Netscape",
	   identity: "Netscape"
	  },
	  {
	   string: navigator.userAgent,
	   subString: "MSIE",
	   identity: "Explorer",
	   versionSearch: "MSIE"
	  },
	  {
	   string: navigator.userAgent,
	   subString: "Gecko",
	   identity: "Mozilla",
	   versionSearch: "rv"
	  },
	  {   // for older Netscapes (4-)
	   string: navigator.userAgent,
	   subString: "Mozilla",
	   identity: "Netscape",
	   versionSearch: "Mozilla"
	  }
	 ],
	 dataOS : [
	  {
	   string: navigator.platform,
	   subString: "Win",
	   identity: "Windows"
	  },
	  {
	   string: navigator.platform,
	   subString: "Mac",
	   identity: "Mac"
	  },
	  {
	      string: navigator.userAgent,
	      subString: "iPhone",
	      identity: "iPhone/iPod"
	     },
	  {
	   string: navigator.platform,
	   subString: "Linux",
	   identity: "Linux"
	  }
	 ]
	
	    };
	    BrowserDetect.init();
	    
	    var browserDetection = BrowserDetect.browser;
	    var browserVersion = 'v' + BrowserDetect.version;
	    var OSname = BrowserDetect.OS;
	    
	    $('body').addClass( browserDetection + ' ' + browserVersion + ' ' + OSname);
	// NAVEGADOR FIX

}
//NAVEGADORES FIX
