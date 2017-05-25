(function() {
    angular.module("ecom", []);
    angular.module("ecom").controller("myCtrl", myCtrl);

    function myCtrl() {
        var vm = this;
        vm.message = "Yeh message controller ke variable mein stored hai";
        vm.backColor = "red";
        vm.counter = 0;
        vm.classChange = function() {
            vm.backColor = vm.backColor === "red" ? "blue" : "red";
        }
        vm.increment = function() {
            vm.counter = vm.counter + 1;
        };

    }
})(window.angular);