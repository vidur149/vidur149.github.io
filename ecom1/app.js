var app = angular.module("ecom", []);
app.controller("myCtrl", function($scope) {

    $scope.message = "Yeh message controller ke variable mein stored hai";
    $scope.backColor = "red";
    $scope.counter = 0;
    $scope.classChange = function() {
        $scope.backColor = $scope.backColor === "red" ? "blue" : "red";
    };
    $scope.increment = function() {
        $scope.counter = $scope.counter + 1;
    };
});