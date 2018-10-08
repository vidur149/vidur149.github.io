angular.module('calc', [])
    .controller("scope1", ["$scope", function($scope) {
        $scope.action = 'Sum';
        $scope.num1 = 0;
        $scope.num2 = 0;
        $scope.result = 0;
        $scope.backColor = "red";

        $scope.callForAction = function() {
            if ($scope.operator === 'sub') {
                $scope.result = $scope.num1 - $scope.num2;
                $scope.action = 'Difference';
            }

            if ($scope.operator === 'add') {
                $scope.result = $scope.num1 + $scope.num2;
                $scope.action = 'Sum';
            }

            if ($scope.operator === 'divis') {
                $scope.result = $scope.num1 / $scope.num2;
                $scope.action = 'Quotient';
            }

            if ($scope.operator === 'mod') {
                $scope.result = $scope.num1 % $scope.num2;
                $scope.action = 'Remainder';
            }

            if ($scope.operator === 'multi') {
                $scope.result = $scope.num1 * $scope.num2;
                $scope.action = 'Product';
            }
        };
    }]);