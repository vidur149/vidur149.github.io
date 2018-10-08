(function() {
    angular.module('auth');
    angular.module('Home');
    angular.module("connect", [
        'auth',
        'Home',
        'ngRoute',
        'ngFileUpload'
    ]);

    angular.module("connect").config(config);

    function config($routeProvider, $qProvider, $locationProvider) {
        $locationProvider.hashPrefix('');
        $qProvider.errorOnUnhandledRejections(false);
        $routeProvider
            .when('/', {
                controller: 'LoginController',
                templateUrl: 'modules/auth/login.html',
                controllerAs: 'vm'
            })
            .when('/home', {
                controller: 'HomeController',
                templateUrl: 'modules/home/home.html',
                controllerAs: 'vm'
            })
            .when('/home/me', {
                controller: 'ProfileController',
                templateUrl: 'modules/home/profile.html',
                controllerAs: 'vm'
            })
            .when('/signup', {
                controller: 'SignupController',
                templateUrl: 'modules/auth/signup.html',
                controllerAs: 'vm'
            })
            .otherwise({ redirectTo: '/' });
    }
})();