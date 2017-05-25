(function() {
    angular.module('auth', ['ngCookies']);
    angular.module('auth').controller('LoginController', LoginController);
    LoginController.$inject = ['$rootScope', '$location', 'AuthenticationService'];

    function LoginController($rootScope, $location, AuthenticationService) {
        var vm = this;
        AuthenticationService.ClearCredentials();
        vm.login = function() {
            vm.dataLoading = true;
            AuthenticationService.Login(vm.username, vm.password, function(response) {
                if (response.data['result'] === true) {
                    AuthenticationService.SetCredentials(vm.username, vm.password);
                    $location.path('/home');
                } else {
                    vm.error = response.data['result'];
                    vm.dataLoading = false;
                    vm.username = '';
                    vm.password = '';
                }
            });
        }
    }

    angular.module('auth').controller('SignupController', SignupController);
    SignupController.$inject = ['$location', 'AuthenticationService'];

    function SignupController($location, AuthenticationService) {
        var vm = this;
        vm.signUp = function() {
            vm.dataLoading = true;
            AuthenticationService.SignUp(vm.username, vm.password, function(response) {
                if (response.data['result'] === true) {
                    console.log(response.data['result']);
                    $location.path('/login');
                } else {
                    vm.error = response.data['result'];
                    vm.dataLoading = false;
                    vm.username = '';
                    vm.password = '';
                }
            });
        }
    }
})();