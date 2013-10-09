			var interval =0;
			$( '#slide-1' ).show();
			//clearInterval ( interval );
			// interval = setInterval ( "move_slider()" , 8000 );
			
			$( '#slider .flexslider' ).flexslider
			({
				animation: "slide",
				useCSS: false,
				touch: false,
				keyboard: false,			
				multipleKeyboard: true,
				pauseOnHover: true,
				slideshow: false,
				directionNav: false,
				video: true,
				animationSpeed: 800,
				animationLoop: true
			});
			
			$( '#controles li a' ).click (
		
			function ( event )
			{
			
				event.preventDefault ( );
				
//				$( this ).parent(  ).hasClass( 'active' );
				if( $( this ).parent(  ).hasClass('active') )
				{
					$( this ).parent(  ).removeClass( 'active' );	
				}
				else
				{
					$( this ).parent(  ).addClass( 'active' );	
				}
				
			}
			);
			
			var ira = 0;
			
	   		var show_animation = true;

			$( '#controles li a' ).click (
		
			function ( event )
			{
			
				event.preventDefault ( );
				
				ira = $( this ).attr ( 'data-link' );
				
				ira = parseFloat ( ira ) ;
				
				//$( '#whatfor' ).addClass( 'claro' );
				
				if( ira > 3  )
				{
					//$( '#whatfor' ).addClass( 'claro' );
				}
				else{
					
					//$( '#whatfor' ).removeClass( 'claro' );	
					
				}
				
				
				
				
				if( $( this ).parent(  ).hasClass('active') )
				{
					$( this ).addClass( 'active' );
				}
				else
				{
					$( this ).parent(  ).addClass( 'active' );	
				}
				
				
				moves_slider ( );
	
				captions ( );
			}
			);
			
			$( '.slide_control' ).click (
					
					function ( event )
					{
					
						event.preventDefault ( );
						
						ira = $( this ).attr ( 'data-link' );
						
						ira = parseFloat ( ira ) ;
						
						//$( '#whatfor' ).addClass( 'claro' );
						
						if( ira > 3  )
						{
							//$( '#whatfor' ).addClass( 'claro' );
						}
						else{
							
							//$( '#whatfor' ).removeClass( 'claro' );	
							
						}
						
						
						
						
						if( $( this ).parent(  ).hasClass('active') )
						{
							$( this ).addClass( 'active' );
						}
						else
						{
							$( this ).parent(  ).addClass( 'active' );	
						}
						
						
						moves_slider ( );
			
						captions ( );
					}
					);

			
			function go_to_slide( ira_ )
			{
				
				show_animation = false;
				clearInterval ( interval );
				ira = parseFloat ( ira_ ) ;
				//$( '#whatfor' ).addClass( 'claro' );
				if( ira > 3  )
				{
				//	$( '#whatfor' ).addClass( 'claro' );
				}
				else{
					
					//$( '#whatfor' ).removeClass( 'claro' );	
					
				}
				
				
				
				
				if( $( this ).parent(  ).hasClass('active') )
				{
					$( this ).addClass( 'active' );
				}
				else
				{
					$( this ).parent(  ).addClass( 'active' );	
				}
				
				
				moves_slider ( );
	
				captions ( );
			}
			
			function captions ( ) 
			{
				var progres_ancho = 80 *  ( ira )  ;
				
				
				$( '#controles #thumb-' + ira ).addClass( 'active' );
				
				if( ira > 2  )
				{
					
					//$( '#whatfor' ).addClass( 'claro' );
					
					//clearInterval ( interval );					
				}
				else{
					
					//$( '#whatfor' ).removeClass( 'claro' );	
					
					//clearInterval ( interval );
					
					//interval = setInterval ( "move_slider()" , 8000 );
					//$( '#progress' )
					
					/*$( '#progress' ).stop ( true , true ).animate ( { 'width' : ira * 80 } , 0 , function ( ) 
					{ 
						$( '#progress' ).animate ( { 'width' : 240 } , 24000 - ira * 8000 ,"linear" ); 
					} );*/
				}
				
				$( '#progress' ).stop ( true , true ).css({ 'width':  progres_ancho } );
				
				if ( ira < 3 )
				{
					//$( '#progress' ).stop ( true , true ).animate ( { 'width' : ira * 80 } , 0 , function ( ) 
					//{ 
					//	$( '#progress' ).animate ( { 'width' : 240 } , 24000 - ira * 8000 ,"linear" ); 
					//} );
				}
				else
				{
					//$( '#progress' ).stop ( true , true ).css({ 'width':  progres_ancho } );	
				}
				
				
				
				$( '#controles li a' ).each( function(i,el)
					{
						//console.log( i )
						
						if( i > ira  )
						{
							$( this ).parent(  ).removeClass( 'active' );	
						}
						else if( i < ira)
						{
							$( this ).parent(  ).addClass( 'active' );
						}
					}
				);
				
			}
			
			function moves_slider ( )
			{
				var slider = $('#slider .flexslider').data('flexslider');
								
				slider.flexAnimate(ira);
				
				$( '.nav-slider .active' ).removeClass ( 'active' );
				
				
			}
			
			/*
			
			*/
			$( '.inner-redes a' ).click (
		
			function ( event )
			{
			
				//event.preventDefault ( );
				
//				$( this ).parent(  ).hasClass( 'active' );
				if( $( this ).hasClass('checked') )
				{
					$( this ).removeClass( 'checked' );	
				}
				else
				{
					$( this ).addClass( 'checked' );	
				}
			}
			);
			$( '.back' ).click (
		
				function ( event )
				{
				
					event.preventDefault ( );
					
					var slidee = $('#slider .flexslider').data('flexslider');
					var actual = slidee.currentSlide;
					slidee.flexAnimate(actual-1);
					thumb_actual  = actual - 1;
					ira = thumb_actual ;
					
					if ( ira  == 2 )
					{
						$( '#whatfor' ).removeClass( 'claro' );
						clearInterval ( interval );
						interval = setInterval ( "move_slider()" , 8000 );
						$( '#progress' ).stop ( true , true ).animate ( { 'width' : ira * 80 } , 0 , function ( ) 
						{ 
							$( '#progress' ).animate ( { 'width' : 240 } , 24000 - ira * 8000 ,"linear" ); 
						} );
					}
					
					$( '#controles #thumb-' + thumb_actual  ).addClass( 'active' );
					
					 progres_ancho = 80 *  (thumb_actual ) ;
				
					$( '#progress' ).css({ 'width':  progres_ancho});
					
					$( '#controles li a' ).each( function(i,el)
					{
						//console.log( i )
						
						if( i > ira  )
						{
							$( this ).parent(  ).removeClass( 'active' );	
						}
						else if( i < ira)
						{
							$( this ).parent(  ).addClass( 'active' );
						}
					}
				);
				}
			
			);
			
			$( '.next' ).click (
		
				function ( event )
				{
				
					event.preventDefault ( );
					
					var slidee = $('#slider .flexslider').data('flexslider');
					var actual = slidee.currentSlide;
					slidee.flexAnimate(actual+1);
					
					thumb_actual  = actual + 1;
					
					$( '#controles #thumb-' + thumb_actual  ).addClass( 'active' );
					
					 progres_ancho = 80 *  (thumb_actual ) ;
				
					$( '#progress' ).css({ 'width':  progres_ancho});
				}
			
			);
			
       
	   		function move_slider( )
			{
				//alert( 'movel' )
					ira ++;
				
					var exampleSlider = $('#slider .flexslider').data('flexslider');
					exampleSlider.flexAnimate(ira);
					captions ( );
					if( ira >= 3 )
					{
						clearInterval ( interval );
					}
									
			}
			$(function() {
			
				$('section.scrollsections').scrollSections({
				createNavigation: false,
				alwaysStartWithFirstSection: true,
				animateScrollToFirstSection:true,		
				touch: false,
				scrollbar: false,
				scrollMax: 0,
				navigation: true,
				keyboard: false,
				before: function($currentSection, $nextSection){
					//alert( $($currentSection).attr('id') )
					 
					
					},
					 after: function($currentSection, $previousSection){
						 if ( $currentSection.attr( 'id' )  == 'whatfor' && show_animation)
						{
							clearInterval ( interval );
							console.log("quilombo");
							interval = setInterval ( "move_slider()" , 8000 );
							$( '#progress' ).stop ( true , true ).animate ( { 'width' : ira * 80 } , 0 , function ( ) 
							{ 
								$( '#progress' ).animate ( { 'width' : 240 } , 24000 - ira * 8000 ,"linear" ); 
							} );
							}
					}
				});
			}
			
		);
		document.ontouchmove = function(e){ 
 		   e.preventDefault(); 
		  // alert( this )
		  //alert( $( this ).attr( 'id' ) )
		}


		$(document).ready(function(){
		  $('#iagree').click(function (event) {
			  console.log("post");
              $.post('/iagree/', {"user_agree":true}, function(data, textStatus){

              }, "json");
		    
		  });
		  

		});
