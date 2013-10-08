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

	// BIG SOCIAL NAV TRIGGER
	//	$('.trigger_social_choice a').click(function (event) {
	//		event.preventDefault();
	//		$(this).parent().parent().parent().addClass('off');
	//		$(this).parent().parent().parent().parent().find('.social_choice').addClass('on');
	//		$(this).parent().parent().parent().parent().find('.confirm_social').addClass('on');
	//		$('.nav_steps').addClass('open_social');
	//	});
		
	//	$('.close_big_nav a').live('click', function (event) {
	//		event.preventDefault();
	//		$('.trigger_social_choice').removeClass('off');
	//		$('.social_choice').removeClass('on');
	//		$('.confirm_social').removeClass('on');
	//		$('.nav_steps').removeClass('open_social');
	//	});
		
	//	$('.confirm_social a').live('click', function (event) {
	//		event.preventDefault();
	//		$('.trigger_social_choice').removeClass('off');
	//		$('.social_choice').removeClass('on');
	//		$('.confirm_social').removeClass('on');
	//		$('.nav_steps').removeClass('open_social');
	//	});
	
	/*$('.nav_big_social li a').live('click', function (event) {
		event.preventDefault();
		$(this).parent().toggleClass('active');
	});*/
	// BIG SOCIAL NAV TRIGGER
        
        
    // SECTOR FIXED NAV
	if ($('.maqueta_new').length) {
		var offsetOne = $('#step_one').offset().top - 150;
        var offsetfive = $('#step_five').offset().top - 150;
        var offseteight = $('#step_eight').offset().top - 150;
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
	// SHARE SOCIAL
	
	// EMAIL SHARE POP-UP
	$('#email_trigger').click(function (event) {
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
		$('#height_slider').slider({
		      range: 'min',
		      value: 0,
		      min: 0,
		      max: 200,
		      slide: function( event, ui ) {
		        var value = ui.value;
		        $('#height_number').html(value);
		      }
		 });	
	}
	// SLIDER NUTRITION
	
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
