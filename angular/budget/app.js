(function() {
    angular.module('budget', ['ui.router', 'angularMoment']);
    angular.module('budget').config(function($stateProvider) {
        var home = {
            name: 'home',
            url: '',
            templateUrl: 'templates/home.html'
        };

        $stateProvider.state(home);
        // var weather = {
        //     name: 'weather',
        //     url: '/weather',
        //     templateUrl: 'templates/weather.html',
        //     controller: 'weatherController'
        // };
    });

    angular.module('budget').controller('somename', somename);



})();