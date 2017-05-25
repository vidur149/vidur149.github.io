(function() {
    angular.module("ecom", []);
    angular.module("ecom").controller("myCtrl", myCtrl);

    function myCtrl() {
        var vm = this;
        vm.cart = [];
        vm.obj = { key: "value" };
        vm.products = [{
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
        vm.addToCart = function(product) {
            vm.cart.push(product);
        };

        vm.removeFromCart = function(product) {
            for (var i = 0; i < vm.cart.length; i++) {
                if (vm.cart[i] === product) {
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
                    total += parseInt(vm.cart[i].price);
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
            replace: true,
            templateUrl: 'product-card.html'
        };

        function link(scope, element, attrs) {
            // scope.my = function() {
            //         console.log(scope);
            //     }
        }
    }

})();