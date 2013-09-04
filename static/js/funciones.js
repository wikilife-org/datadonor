if (typeof console == "undefined") var console = { log: function() {} };

$(document).ready(function () {
//READY START

	exploradorVersion();

	// BIG SOCIAL NAV TRIGGER
	$('.trigger_social_choice a').click(function (event) {
		event.preventDefault();
		$('.trigger_social_choice').addClass('off');
		$('.social_choice').addClass('on');
		$('#confirm_social').addClass('on');
	});
	$('#close_big_nav a').live('click', function (event) {
		event.preventDefault();
		$('.trigger_social_choice').removeClass('off');
		$('.social_choice').removeClass('on');
		$('#confirm_social').removeClass('on');
	});
	$('#confirm_social a').live('click', function (event) {
		event.preventDefault();
		$('.trigger_social_choice').removeClass('off');
		$('.social_choice').removeClass('on');
		$('#confirm_social').removeClass('on');
	});
	// BIG SOCIAL NAV TRIGGER		
	
	// NAV BIG SOCIAL
	$('#nav_big_social li a').live('click', function (event) {
		//event.preventDefault();
		$(this).parent().toggleClass('active');
	});
	// NAV BIG SOCIAL 
	
	// SECTOR FIXED NAV
	if ($('.scroll_fixed_trigger').length) {
		
		$(window).scroll(function(){
		  
			  // container height
			  var h = $('#container').height();
			  var y = $(window).scrollTop();
			  
			  // Offsets
			  var fixedNav = $('.step_one').offset().top;
			
			  // efect
			  if( y > fixedNav ){
				
				$('.nav_steps').addClass('fixed');

			  } else {
			  	
			  	$('.nav_steps').removeClass('fixed');
			  	
			  }
		  
		 });	
		 
	}
	
	// SCROLL SOLO
	$('.nav_steps a').click(function (event) {
		event.preventDefault();
		
		var scrollTo = $(this).attr('data-scroll');
		
		// scroll to
		$('html, body').stop(true,true)
		$('html, body').animate({
			scrollTop: $('#'+scrollTo).offset().top
		}, 1500);
		
		// ie8 fix
		$(document).stop(true,true)
		$(document).animate({
			scrollTop: $('#'+scrollTo).offset().top
		}, 1500);
		
		
	});
	// SCROLL SOLO
	
	// SECTOR FIXED NAV


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
	console.log(windowWidth);
	
	if (windowWidth < 1280) {
	
		$('.nav_steps').css({left:"20px"});
		console.log("menos de 1280");
		
	} else {
	
		var leftMargin = windowWidth - 1050;
		var distanciaNav = leftMargin/2;
		var margenFinal = distanciaNav - 100;
		
		$('.nav_steps').css({left: margenFinal+"px"});
		
		console.log("mas de 1280");
		
	}
	
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
