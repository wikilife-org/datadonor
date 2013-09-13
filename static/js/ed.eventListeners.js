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