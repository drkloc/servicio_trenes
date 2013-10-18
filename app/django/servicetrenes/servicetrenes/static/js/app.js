
$(document).ready(function(){
    var trenes = io.connect(socket_server);
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

Ember.Handlebars.helper('format-arrivals', function(arrivals){
    var context;
    var render = '';
    var t = Handlebars.compile(
        '<span class="{{classes}}">{{label}}</span>'
    );
    $.each(arrivals, function(i){
        if (arrivals[i] === 0){
            context = {
                classes: 'badge badge-success',
                label: 'En andén'
            };
        }else{
            context = {
                classes: 'badge',
                label: arrivals[i]
            };
            if(context.label < 15){
                context.classes += ' badge-warning';
            }else{
                context.classes += ' badge-important';
            }
        }
        render += ' ' + t(context);
    });
    return new Handlebars.SafeString(render);
});

Ember.Handlebars.helper('estacion-destino', function(estaciones){
    return estaciones[estaciones.length-1].estacion;
});

Ember.Handlebars.helper('estacion-origen', function(estaciones){
    return estaciones[0].estacion;
});