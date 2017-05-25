(function() {
    angular.module('Home').factory('TimelineService', TimelineService);
    TimelineService.$inject = ['$http', '$rootScope', '$cookieStore', '$q', 'Upload'];

    function TimelineService($http, $rootScope, $cookieStore, $q, Upload) {
        service = {};
        service.GetPosts = function() {
            var defer = $q.defer();
            $http.get('http://localhost:5000/allposts').then(function(response) {
                defer.resolve(response.data['posts']);
            });
            return defer.promise;
        }
        service.GetMyPosts = function() {
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
                defer.resolve(response.data['comment']);
            }, function(error) {
                defer.resolve(error);
            });
            return defer.promise;
        }

        service.CommentOnComment = function(content, postid, commentid) {
            var defer = $q.defer();
            $http.post('http://localhost:5000/posts/' + postid + '/comment/' + commentid, { content: content }).then(function(response) {
                defer.resolve(response.data['comment']);
            }, function(error) {
                defer.resolve(error);
            });
            return defer.promise;
        }

        service.Upload = function(file) {
            var defer = $q.defer();
            file.upload = Upload.upload({
                url: 'http://localhost:5000/user/upload/profilepicture',
                data: { file: file },
            });

            file.upload.then(function(response) {
                if (response.data['result'] === true) {
                    defer.resolve("Successfully Uploaded");
                }
            }, function(response) {
                if (response.status > 0) {
                    defer.resolve(response.data['result']);
                }
            });
            return defer.promise;
        }

        return service;
    }
})();