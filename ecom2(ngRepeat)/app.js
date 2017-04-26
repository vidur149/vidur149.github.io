var app = angular.module("ecom", []);
app.controller("myCtrl", function($scope) {
    $scope.cart = [];
    $scope.products = [{
        name: "Moto G5",
        price: "18000",
        type: "mobiles"
    }, {
        name: "Oppo F1s",
        price: "16000",
        type: "mobiles"
    }, {
        name: "Harry Potter Collection",
        price: "10000",
        type: "books"
    }, {
        name: "cello fullPower",
        price: "10",
        type: "stationery"
    }];
    $scope.addToCart = function(product) {
        $scope.cart.push(product);
        console.log($scope.cart);
    };

    $scope.removeFromCart = function(product) {
        for (var i = 0; i < $scope.cart.length; i++) {
            if ($scope.cart[i] === product) {
                if (i > -1) {
                    $scope.cart.splice(i, 1);
                }
                break;
            }
        }
    }

    $scope.cartValue = function() {
        var total = 0;
        if ($scope.cart.length > 0) {
            for (var i = 0; i < $scope.cart.length; i++) {
                total += parseInt($scope.cart[i].price);
            }
        }
        return total;
    }
});