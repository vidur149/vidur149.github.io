(function() {
    angular.module('Home', []);

    angular.module('Home').controller('HomeController', HomeController);
    angular.module('Home').filter('dateFilter', function() {
        return function(input) {
            var date;
            date = moment(input).utcOffset('+0000').format("MMMM Do YYYY, h:mm:ss");
            return date;
        };
    });
    HomeController.$inject = ['TimelineService'];

    function HomeController(TimelineService) {
        var vm = this;
        vm.dataLoading = false;

        vm.posts = [];
        TimelineService.SetCredentials();
        TimelineService.GetPosts().then(function(response) {
            vm.posts = response;
        });
        vm.post = function() {
            TimelineService.PostPosts(vm.content).then(function(response) {
                vm.dataLoading = false;
                vm.content = '';
                vm.posts.push(response['post']);
            });
        };

        vm.like = function(postid) {
            console.log('hey');
            TimelineService.Like(postid).then(function(response) {
                for (var i = 0; i < vm.posts.length; i++) {
                    if (vm.posts[i]['id'] === postid) {
                        vm.posts[i]['total_likes'] = response;
                        break;
                    }
                }
            });
        }
        vm.comment = function(post) {
            TimelineService.Comment(post['new_comment'], post['id']).then(function(response) {
                for (var i = 0; i < vm.posts.length; i++) {
                    if (vm.posts[i]['id'] === post.id) {
                        vm.posts[i]['comments'].push(response);
                        post['new_comment'] = '';
                        break;
                    }
                }
            });
        }
        vm.commentOnComment = function(post, comment) {
            TimelineService.CommentOnComment(comment['new_nested_comment'], post['id'], comment['id']).then(function(response) {
                for (var i = 0; i < vm.posts.length; i++) {
                    if (vm.posts[i]['id'] === post['id']) {
                        for (var j = 0; j < vm.posts[i]['comments'].length; j++) {
                            if (vm.posts[i]['comments'][j]['id'] === comment.id) {
                                vm.posts[i]['comments'][j]['comments'].push(response);
                                comment['new_nested_comment'] = '';
                                break;
                            }
                        }
                    }
                }
            });
        }
    }
    angular.module('Home').controller('ProfileController', ProfileController);

    ProfileController.$inject = ['TimelineService', 'Upload'];

    function ProfileController(TimelineService, Upload) {
        var vm = this;
        vm.dataLoading = false;
        vm.myposts = [];
        TimelineService.SetCredentials();
        TimelineService.GetMyPosts().then(function(response) {
            vm.myposts = response;
        });

        vm.uploadPic = function(file) {
            vm.picFile = "";
            file.upload = Upload.upload({
                url: 'http://localhost:5000/user/upload/profilepicture',
                data: { file: file },
            });

            file.upload.then(function(response) {
                if (response.data['result'] === true) {
                    vm.message = "successfully uploaded"
                }
            }, function(response) {
                if (response.status > 0) {
                    vm.message = response.data['result'];
                }
            });
        }

        vm.post = function() {
            TimelineService.PostPosts(vm.content).then(function(response) {
                vm.dataLoading = false;
                vm.content = '';
                vm.myposts.push(response['post']);
            });
        };

        vm.like = function(postid) {
            console.log('hey');
            TimelineService.Like(postid).then(function(response) {
                for (var i = 0; i < vm.myposts.length; i++) {
                    if (vm.myposts[i]['id'] === postid) {
                        vm.myposts[i]['total_likes'] = response;
                        break;
                    }
                }
            });
        }
        vm.comment = function(post) {
            TimelineService.Comment(post['new_comment'], post['id']).then(function(response) {
                for (var i = 0; i < vm.myposts.length; i++) {
                    if (vm.myposts[i]['id'] === post.id) {
                        vm.myposts[i]['comments'].push(response);
                        post['new_comment'] = '';
                        break;
                    }
                }
            });
        }
        vm.commentOnComment = function(post, comment) {
            TimelineService.CommentOnComment(comment['new_nested_comment'], post['id'], comment['id']).then(function(response) {
                for (var i = 0; i < vm.myposts.length; i++) {
                    if (vm.myposts[i]['id'] === post['id']) {
                        for (var j = 0; j < vm.myposts[i]['comments'].length; j++) {
                            if (vm.myposts[i]['comments'][j]['id'] === comment.id) {
                                vm.myposts[i]['comments'][j]['comments'].push(response);
                                comment['new_nested_comment'] = '';
                                break;
                            }
                        }
                    }
                }
            });
        };
    }
})();