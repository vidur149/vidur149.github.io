(function() {
    angular.module('Home').factory('MessageService', MessageService);
    MessageService.$inject = ['$http', '$rootScope', '$cookieStore', '$q'];

    function MessageService($http, $rootScope, $cookieStore, $q) {
        service = {};
        service.GetPeople = function() {
            var defer = $q.defer();
            $http.get('http://localhost:5000/users').then(function(response) {
                defer.resolve(response.data['users']);
            });
            return defer.promise;
        }
        service.SetCredentials = function() {
            user = $cookieStore.get('globals');
            authdata = user['currentUser']['authdata'];
            $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata;
        };

        service.GetMessages = function(name) {
            var defer = $q.defer();
            $http.get('http://localhost:5000/messages/' + name).then(function(response) {
                defer.resolve(response.data['messages']);
            });
            return defer.promise;
        }

        service.SendMessage = function(message, person) {
            var defer = $q.defer();
            $http.post('http://localhost:5000/messages/' + person, { content: message }).then(function(response) {
                defer.resolve(response.data);
            }, function(error) {
                defer.resolve(error);
            });
            return defer.promise;
        };
        return service;
    }
})();