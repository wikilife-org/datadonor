
//v1.0

/*
- si hago scroll rapido...no llega a resetear los navs.
- podria optimizar la parte de los calculos
- podria poner algun estado como para ahorrarme los calculos?
*/

/*
como se implementa:
<div id="unID" class="sticky">Contenido</div>
necesita que se cargue antes : ed.eventListeners.js
*/

// !EVENT LISTENER
var EventListener = function(){
	this.suscribers_array = new Array();
};
// !properties
//EventListener.prototype.suscribers_array = new Array();
// !metods
EventListener.prototype.suscribe = function( instance_n , event_n , method_n){
	this.suscribers_array.push({ instance : instance_n , event_listener : event_n , method : method_n})
	
}
EventListener.prototype.broadcast = function(event_listener,params){
	for(i=0;i<this.suscribers_array.length;i++){
		var item = this.suscribers_array[i];
		if( item.event_listener == event_listener ){
			//fire event
			var instance = this.suscribers_array[i].instance; 
			instance[this.suscribers_array[i].method](params)
		}
	}
}
EventListener.prototype.getInstance = function(pos){
	return this.suscribers_array[pos];
}

//---------------------------------

stickyListeners = new EventListener();


// !LISTAS LISTENER
var StickyHeader = function(id,pos){
	this.id = id;
	this.originalY = $('#'+id).position().top;
	this.el = $('#'+id);
	this.pos = pos;
	this.ratio = 0; //this.el.outerHeight()/3;
	//suscribe la instancia a los listeners
	stickyListeners.suscribe( this , 'onScrollUpdate' , 'checkStickyness'); 
};

// !methods
StickyHeader.prototype.checkStickyness = function(){
	
	//ayuda para el calculo
	if(this.pos==0){ 
		var topPos = 0;
		var break_point = this.originalY;
	}else{
		var prev_el_height = $('#'+stickyListeners.getInstance(this.pos-1).instance.id).outerHeight();
		var prev_el_top = $('#'+stickyListeners.getInstance(this.pos-1).instance.id).css('top');
		var topPos = prev_el_height + Number(prev_el_top.replace('px',''));
		var break_point = this.originalY - topPos;
	}
	
	// checkea si se hace sticky
	if( $(window).scrollTop() > break_point && !this.el.hasClass('collapsed')){
		//agrega div para que no salte el scroll
		this.el.parent().prepend('<div id="'+this.id+'_sticky" style="display:block;height:'+this.el.outerHeight()+'px" > </div>');
		//agrega clase
		this.el.addClass('collapsed');
		//setea de estilos
		this.el.css('position','fixed');
		this.el.css('z-index','9999');
		this.el.css('top','0px');
//		this.el.css('top',topPos+'px');
		this.updateNav()
	}
	
	// checkea si se vuelve a la normalidad
	if( $(window).scrollTop() < break_point && this.el.hasClass('collapsed') ){
		//saca el div que ayudaba a que no salte el scroll
		$('#'+this.id+'_sticky').remove();
		//saca la clase
		this.el.removeClass('collapsed');
		//resetea los estilos
		this.el.css('position','static');
		this.el.css('z-index','auto');
		this.el.css('top','auto');
		this.updateNav()
	}
	
}


StickyHeader.prototype.updateNav = function(){
	
	var activate_class = $('.sticky.collapsed').last().data('step_nav');
	$('.nav_steps .nav a').parent().removeClass("active");
	$('.'+activate_class).parent().addClass('active');
		    	
    var anchorVal = $('.'+activate_class).attr('href');
    if(typeof(anchorVal)=="undefined"){
    	location.hash = "#";
    }else{
    	location.hash = anchorVal;
    }
    
}

// !init crea una isntancia de por cada StickyHeader .sticky
$(function() {

	var i = 0;
	$('.sticky').each(function(){
		var item_id = $(this).attr('id');
		new StickyHeader(item_id,i);
		i++;
	})
	$(window).scroll(function(){
		stickyListeners.broadcast('onScrollUpdate');
	});
	
})

