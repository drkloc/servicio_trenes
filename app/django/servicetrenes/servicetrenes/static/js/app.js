
$(document).ready(function(){
    var trenes = io.connect('http://localhost:9000');
    trenes.on('connect', function() {
        console.log('connected to socket');
        trenes.emit("subscribe");
        console.log('subscribing');
    });
    trenes.on('disconnect', function(){
        console.log('connected to socket');
    });
    trenes.on('proximos trenes', function(data){
        $.each(data, function(i){
            var o = lineas.findBy(
                'nombre', this.linea
            ).estaciones.findBy(
                'estacion', this.estacion
            );
            Ember.set(o, 'proximos_destino', this.proximos_destino);
            Ember.set(o, 'proximos_origen', this.proximos_origen);
        });
    });
});

App = Ember.Application.create();

App.Router.map(function(){
    this.resource('lineas', {path: '/'}, function(){
        this.resource('linea', { path: ':nombre'});
    });
});

App.LineasRoute = Ember.Route.extend({
    model: function(){
        return lineas;
    }
});

App.LineaRoute = Ember.Route.extend({
    model: function(params){
        return lineas.findBy('nombre', params.nombre);
    }
});

Ember.Handlebars.helper('format-minutes', function(m){
    if(m.length){
        $.each(m, function(i){
            m[i] = moment().add('minutes', m[i]).fromNow(true);
        });
        return m;
    }else{
        return 'No trains';
    }
});