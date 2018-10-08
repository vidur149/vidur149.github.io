(function() {
    angular.module('Home').controller('HomeController', HomeController);
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

})();