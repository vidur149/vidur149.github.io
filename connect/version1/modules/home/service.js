(function() {
    angular.module('Home').factory('TimelineService', TimelineService);
    TimelineService.$inject = ['$http', '$rootScope', '$cookieStore', '$q'];

    function TimelineService($http, $rootScope, $cookieStore, $q) {
        service = {};
        service.GetPosts = function() {
            var defer = $q.defer();
            $http.get('http://localhost:5000/posts').then(function(response) {
                defer.resolve(response.data['posts']);
            });
            return defer.promise;
        }

        service.PostPosts = function(content) {
            var defer = $q.defer();
            $http.post('http://localhost:5000/posts', { content: content }).then(function(response) {
                console.log(response);
                defer.resolve(response.data);
            }, function(error) {
                defer.resolve(error);
            });
            return defer.promise;
        }

        service.Like = function(postid) {
            var defer = $q.defer();
            $http.post('http://localhost:5000/posts/' + postid + '/like').then(function(response) {
                defer.resolve(response.data['likes']);
            }, function(error) {
                console.log(error);
            });
            return defer.promise;
        }

        service.GetUser = function() {
            user = $cookieStore.get('globals');
            return user['currentUser']['username'];
        }
        service.SetCredentials = function() {
            user = $cookieStore.get('globals');
            authdata = user['currentUser']['authdata'];
            $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata;
        };

        service.Comment = function(content, postid) {
            var defer = $q.defer();
            $http.post('http://localhost:5000/posts/' + postid + '/comment', { content: content }).then(function(response) {
                console.log(response);
                defer.resolve(response.data['comment']);
            }, function(error) {
                defer.resolve(error);
            });
            return defer.promise;
        }

        return service;
    }
})();