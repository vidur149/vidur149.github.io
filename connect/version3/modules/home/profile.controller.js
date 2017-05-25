(function() {
    angular.module('Home').controller('ProfileController', ProfileController);

    ProfileController.$inject = ['TimelineService'];

    function ProfileController(TimelineService) {
        var vm = this;
        vm.dataLoading = false;
        vm.myposts = [];
        TimelineService.SetCredentials();
        TimelineService.GetMyPosts().then(function(response) {
            vm.myposts = response;
        });

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

        vm.uploadPic = function(file) {
            vm.picFile = "";
            TimelineService.Upload(file).then(function(response) {
                console.log(response);
                vm.message = response;
            });
        }
    }


})();