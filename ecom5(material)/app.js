(function() {
    angular.module("ecom", ['ngMaterial']).config(config);
    angular.module("ecom").controller("myCtrl", myCtrl);

    function config($mdThemingProvider) {
        console.log("hry");
        $mdThemingProvider.theme('dark-color').backgroundPalette('orange').dark();
    }

    function myCtrl() {
        var vm = this;
        vm.cart = [];
        vm.obj = { key: "value" };
        vm.orderByMe = "type";
        vm.products = [{
            name: "Moto G5",
            price: "18000",
            type: "mobiles",
            qty: 1
        }, {
            name: "Oppo F1s",
            price: "16000",
            type: "mobiles",
            qty: 1
        }, {
            name: "Harry Potter Collection",
            price: "10000",
            type: "books",
            qty: 1
        }, {
            name: "cello fullPower",
            price: "10",
            type: "stationery",
            qty: 1
        }];
        vm.addToCart = function(product) {
            if (vm.cart.length === 0) {
                vm.cart.push(product);
                return;
            }
            var flag = 0;
            for (var i = 0; i < vm.cart.length; i++) {
                if (vm.cart[i] == product) {
                    vm.cart[i].qty = parseInt(vm.cart[i].qty) + 1;
                    break;
                } else {
                    console.log("e312");
                    flag++;
                }
            }
            if (flag === vm.cart.length) {
                vm.cart.push(product);
                vm.cart[i].qty = 1;
            }
        };

        vm.removeFromCart = function(product) {
            for (var i = 0; i < vm.cart.length; i++) {
                if (vm.cart[i] === product) {
                    product.qty = 0;
                    if (i > -1) {
                        vm.cart.splice(i, 1);
                    }
                    break;
                }
            }
        }

        vm.cartValue = function() {
            var total = 0;
            if (vm.cart.length > 0) {
                for (var i = 0; i < vm.cart.length; i++) {
                    total += (parseInt(vm.cart[i].price) * vm.cart[i].qty);
                }
            }
            return total;
        }
    }
    angular.module("ecom").directive("productCard", productCard);

    function productCard() {
        // return the directive definition object 
        return {
            scope: {
                product: '=',
                add: '&'
            },
            transclude: true,
            link: link,
            // replace: true,
            templateUrl: 'product-card.html'
        };

        function link(scope, element, attrs) {
            // scope.my = function() {
            //         console.log(scope);
            //     }
        }
    }

})();