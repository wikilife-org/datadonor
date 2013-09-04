var array = [];

var g = true;
var t = 0;
function lights_out ( )
{
	
	if ( g == true )
	{
		
		//alert("si")
		$( '.pause' ).stop ( true , true ).animate ( { opacity: 0 } );
		g = false;
	}
	
}

$( document ).ready (

	function ( )
	{
		var scrollTop = $( window ).scrollTop ( );
		
		$(".pause").live("hover mousemove", function(e) {
			$( '.pause' ).stop ( true , true ).animate ( { opacity: 1 } );
			g = true;
			t = setTimeout ( "lights_out ( )" , 1000 );
			//clearTimeout ( t );
 			$( this ).css ( { opacity: 1 } );
		});
			
			
			
			//centrar_row2 ( );
		
		
		
		$('#header-top, #header-top video, #header-top .flexslider, #header-top .flexslider li').css( { height: $(window).height() } );
		//scroll_nav ( );
		//$( '#progress' ).stop ( true , true ).animate ( { 'width' : slide_actual * 240 } , 0 , function ( ) { $( '#progress' ).animate ( { 'width' : 960 } , 16000 - slide_actual * 4000 ,"linear" ); } );
		
		mon_resize();
		//centrar_row2 ( );
		
		
		$( window ).load ( 
			function ( )
			{	
			//centrar_row2 ( );
			});
		interval2 = setInterval ( "imgshow()" , 500 );
		//imgshow()
		
		
		
		
		var video_1 = true;
		
		$( '#header-top .next-video' ).click(function( e )
		{
			
			//e.preventDefault();
			if( video_1 == true )
			{
				
				$( '.watch-video' ).removeAttr('id');
				$( '.watch-video' ).attr( 'id', 'video-02'); 
				$( '.watch-video, .pause' ).removeAttr('onClick')
				$( '.watch-video, .pause' ).attr( 'onClick', 'playPause2()'); 
				
				video_1 = false;
			}
			else
			{
				$( '.watch-video' ).removeAttr('id');
				$( '.watch-video' ).attr( 'id', 'video-01');
				$( '.watch-video, .pause' ).removeAttr('onClick')
				$( '.watch-video, .pause' ).attr( 'onClick', 'playPause()'); 
				
				
				video_1 = true;
			}
			
		});
		
		$( '#header-top .watch-video' ).click(function( e )
		{

			e.preventDefault();
			if( video_1 == true )
			{
				$( '#header-top video' ).hide();
			
				$( '#video-top' ).fadeIn();
				
			}
			else
			{
				$( '#header-top video' ).hide();
			
				$( '#video-top2' ).fadeIn();	
			}
			
			//$( this ).hide();
			//playPause();
			

		});
		
		//centrar_row2 ( );
		$(window).resize ( function ( ) 
		{
			
			mon_resize ( );
			centrar_row2 ( );
			$( '#header-top' ).css({ 'height': $(window).height() });
			//var altop = $(window).height();
			//alert(altop)
			
			
		});	
		
		
		var isiPad = navigator.userAgent.match(/iPad/i) != null;
		
		$( window ).scroll ( 
			function ( )
			{	

			
				scrollTop = $( window ).scrollTop ( );
				
				
				if( scrollTop >= $(window).height()  )
				{
					$( '#header' ).addClass( 'fixed' );
				}
				else
				{
					// $( '#header' ).addClass( 'fixed' );
					$( '#header' ).removeClass( 'fixed' );
				
				}
			}
		
		);
		
		
		
		
	}
	
);

function scrolTo ( el ) 
{

	$('html, body').animate({
		scrollTop: $('#'+el.attr('data-loc')).offset().top - 50
		//scrollTop: $('#'+ele.attr('data-loc')).offset().top - (ab.main.vars.device != 'mobile' ? 55 : '')
	}, 500);
}


function Viewport ( )
{
	
  fViewport();
  $(window).bind("scroll", function(event) {fViewport();}); //end scroll
  $(window).resize(function(){fViewport();});

  function fViewport( )
  {
    
	$("section:in-viewport").each( function( ) 
	{
		$(this).addClass("animate");
		/*if($( this ).attr('id') == 'section-counter' ) 
		{
			 $( 'nav a' ).attr( 'data-scroll, how-to-share'  ).addClass( 'active' );
		}*/

	});
		/*$("#how-to-share:in-viewport").each( function( ) 
		{
		$( '#how-to-share .flexslider' ).flexslider({slider.play()});
		});*/

   
  }//end function  fViewport()

}//end function openViewoirt()


function centrar_row2 ( )
{
	var alto_img = $( '#second img' ).height();
	//$( '#second .right' ).removeAttr("height")
	$( '#second .right' ).css( { height: alto_img } );
	var altg =$(window).height() -115; 
		$( '.footer-path' ).css({ height: altg });
	
}




function img_footer( )
{
	(function($) {
            var cache = [];
            $.preLoadImages = function() {
             var args_len = arguments.length;
              for (var i = args_len; i--;) {
                var cacheImage = document.createElement('img');
                cacheImage.src = arguments[i];
                cache.push(cacheImage);
              }
           }
          })(jQuery)
		  
        jQuery.preLoadImages("/static/img/img-1.jpg", "/static/img/img-2.jpg", "/static/img/img-3.jpg", "/static/img/img-4.jpg", "/static/img/img-5.jpg", "/static/img/img-6.jpg");
        imgLoop = "";
		imgLoop2 = "";
		imgLoop3 = "";
        //$("#img-cont-1").show();
        //$(".img-loop").hide();
        $("#img-cont-1").css("z-index","25");
		
        $(window).load(function(){

            $("#logo-img-container-1 .img-loop").hide();
            $("#logo-img-container-1 .img-fondo-loop").css("display", "none");
            $("#img-cont-1").show();
			
            $("#mascara-container").on("mouseenter",function(){
                $(".img-container #img-cont-1 img").css("visibility", "hidden");
                $("#logo-img-container-1 .img-fondo-loop").css("display", "block");
                $("#logo-img-container-1 .img-loop img").css("visibility", "visible");
                imgLoop=setInterval(imgNext,110);
            });
            $("#mascara-container").on("mouseleave",function(){
                clearInterval(imgLoop);
                imgLoop="";
                $("#logo-img-container-1 .img-loop img").css("visibility", "hidden");
                $("#logo-img-container-1 .img-fondo #img-logo").css("display", "block");
                $("#logo-img-container-1.img-container #img-cont-1 img").css("visibility", "visible");

            });
			
			$("#logo-img-container-2 .img-loop").hide();
            $("#logo-img-container-2 .img-fondo-loop").css("display", "none");
            $("#img-cont-1").show();
			
            $("#mascara-container-2").on("mouseenter",function(){
                $(".img-container #img-cont-2 img").css("visibility", "hidden");
                $("#logo-img-container-2 .img-fondo-loop").css("display", "block");
                $("#logo-img-container-2 .img-loop img").css("visibility", "visible");
                imgLoop2=setInterval(imgNext2,110);
            });
            $("#mascara-container-2").on("mouseleave",function(){
                clearInterval(imgLoop2);
                imgLoop2="";
                $("#logo-img-container-2 .img-loop img").css("visibility", "hidden");
                $("#logo-img-container-2 .img-fondo #img-logo").css("display", "block");
                $("#logo-img-container-2.img-container #img-cont-2 img").css("visibility", "visible");

            });
			
			$("#logo-img-container-3 .img-loop").hide();
            $("#logo-img-container-3 .img-fondo-loop").css("display", "none");
            $("#img-cont-3").show();
			
            $("#mascara-container-3").on("mouseenter",function(){
                $(".img-container #img-cont-3 img").css("visibility", "hidden");
                $("#logo-img-container-3 .img-fondo-loop").css("display", "block");
                $("#logo-img-container-3 .img-loop img").css("visibility", "visible");
                imgLoop3=setInterval(imgNext3,150);
            });
            $("#mascara-container-3").on("mouseleave",function(){
                clearInterval(imgLoop3);
                imgLoop3="";
                $("#logo-img-container-3 .img-loop img").css("visibility", "hidden");
                $("#logo-img-container-3 .img-fondo #img-logo").css("display", "block");
                $("#logo-img-container-3.img-container #img-cont-3 img").css("visibility", "visible");

            });
        });

        function imgNext() {
        $("#logo-img-container-1 .img-fondo-loop:first").show().next(".img-fondo-loop").hide().end().appendTo("#logo-img-container-1");
        }
		function imgNext2() {
        $("#logo-img-container-2 .img-fondo-loop:first").show().next(".img-fondo-loop").hide().end().appendTo("#logo-img-container-2");
        } 
		function imgNext3() {
        $("#logo-img-container-3 .img-fondo-loop:first").show().next(".img-fondo-loop").hide().end().appendTo("#logo-img-container-3");
        } 
		
		
		
}

function scroll_nav ( )
{
	$( 'nav a, .goto' ).click(function( e )
		{
			e.preventDefault();
			
			var este = $( this ).attr( 'data-scroll' ) ;
			
			topmover($( '.section-'+este ))
			
		}
	);
	
}
var ancorabout ;
var ancorfour;
var ancorconuter ;
var ancor_how_to_share;

function ancor_point ( )
{
	/*
	ancorabout = $( '.section-about' ).offset().top-105 ;
	console.log ( 'about'+ ancorabout )
	ancorfour = $( '#four' ).offset().top-105;
	console.log ( 'four'+ ancorfour )
	ancorconuter = $( '#section-counter' ).offset().top-105;
	console.log ( 'counter'+ ancorconuter )
	ancor_how_to_share = $( '#how-to-share' ).offset().top-105;
	console.log ( 'how to share'+ ancor_how_to_share )
	
	*/		
	//$(window).height();
	var nuevoAlt = $(window).height() ;
	
	ancorabout = nuevoAlt * 1 -2 ;
	console.log ( 'about'+ ancorabout )
	ancorfour = ( nuevoAlt * 2 ) - 101 ;
	console.log ( 'four'+ ancorfour )
	ancorconuter = ( nuevoAlt * 3 ) - 101 * 2 ; 
	console.log ( 'counter'+ ancorconuter )
	ancor_how_to_share =  ( nuevoAlt * 4 ) -101 * 3;
	console.log ( 'how to share'+ ancor_how_to_share )
}
function topmover(topthis)
{
   		var scrollTop = $(window).scrollTop(),
        elementOffset = topthis.offset().top,
        distance1 = (elementOffset - scrollTop);
   		distance = (distance1 - 100);
		
   		
        $('html, body').animate({
            scrollTop: $(window).scrollTop() + distance
         }, { duration: 500, queue: false });
}


function mon_resize() {	
	newW = $(window).width();
	newH = 360/640*newW;
	newL = 0;
	newT = $(window).height()/2-newH/2;
	if(newH<$(window).height()) {
		newH = $(window).height();
		newW = 640/360*newH;
		newL = $(window).width()/2-newW/2;
		newT = 0;
	}
	$('.wrapper video').css({'width': newW+'px', 'height': newH+'px', 'left': newL+'px', 'top': newT+'px'});
	$( '#header-top li, #header-top li img ' ).css({ 'height': newH +'px', 'width': newW+'px' });
	//$('.f').css({'width': $(window).width()+'px', 'height': $(window).height()+'px'});
}

function alto_seccion ( )
{
	$(".seccion").each( function( ) 
		{
			if( $(window).width() > '1200' )
				{
				
					$(this).css( { height: $( window ).height( ) -100 } );
					var alt = $( this ).find( '.center-v' ).height( ) ;
					//console.log ( alt/2 );
					alt = -alt/2;
					$( this ).find( '.center-v' ).css({ 'marginTop':  alt+'px'});
					//$( '#second .center' ).css({ 'marginTop':  -  +'250px' });
					
				}
				else
				{
					//$(this).css( { height: 'inherit' } );
				}
		});
		
	
}
function imgshow()
		{
			var number1 = 1 + Math.floor(Math.random() * 9);
			var number = 1 + Math.floor(Math.random() * 9);
			number=number1+''+number;
			//alert(number)
			//alert( number1+ '' + number )
			//$( '.cuadro' ).hide();
			$(".cuadro").each( function( i ) 
			{
				//alert(number)
				if( i == number )
				{
					//alert( 'ss' )
					if( $( this ).hasClass( 'oculto' ) )
					{
						$( this ).removeClass( 'oculto' );
						$( this ).find( '.img' ).fadeOut();
					}
					else{
						$( this ).addClass( 'oculto' );
						$( this ).find( '.img' ).fadeIn();	
					}
				}
			});	
		}