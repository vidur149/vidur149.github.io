(function() {
    angular.module('Home', []);

    angular.module('Home').controller('HomeController', HomeController);
    angular.module('Home').filter('dateFilter', function() {
        return function(input) {
            var date;
            date = moment(input).utcOffset('+0000').format("MMMM Do YYYY, h:mm:ss");
            console.log(date);
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
    }


})();