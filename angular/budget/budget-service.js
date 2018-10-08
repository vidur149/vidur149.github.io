(function() {
    angular.module("budget").factory("budgetService", ["$http", function($http) {
        return {
            getCompleteBudget: function() {
                return $http.get("http://localhost:3000/budget").then(function(response) {
                    return response.data;
                })
            },

            getMonthlyBudget: function(month) {
                return $http.get("http://localhost:3000/budget?month=" + month).then(function(response) {
                    return response.data[0];
                })
            },

            getMonthlyExpense: function(month) {
                return $http.get("http://localhost:3000/expense?month=" + month).then(function(response) {
                    console.log(response.data);
                    return response.data;
                })
            },

            getAllCategories: function() {
                return $http.get("http://localhost:3000/category").then(function(response) {
                    return response.data;
                });
            },

            updateBudget: function(obj, id) {
                return $http.put("http://localhost:3000/budget/" + id, obj).then(function(response) {
                    return response.data;
                });
            },

            addExpense: function(obj) {
                return $http.post("http://localhost:3000/expense", obj).then(function(response) {
                    return response.data;
                });
            }
        };
    }]);
})();