(function() {
    angular.module('budget', ['ui.router', 'angularMoment', 'chart.js'])
        .config(function($stateProvider, ChartJsProvider) {
            ChartJsProvider.setOptions({
                chartColors: ['#6495ed', '#FF8A80'],
                responsive: false
            });
        });

    angular.module('budget').controller('budgetController', budgetController);
    budgetController.$inject = ['budgetService', '$timeout'];

    function budgetController(budgetService, $timeout) {

        var that = this;
        var currentDate = new Date();
        that.currentDate = currentDate;
        var month = currentDate.getMonth();
        that.currentDay = currentDate.getDate();
        var daysInMonth = new Date(currentDate.getFullYear(), month, 0).getDate();
        that.daysLeft = daysInMonth - that.currentDay - 1;
        that.showExpenseForm = false;

        that.options = {
            scales: {
                xAxes: [{
                    ticks: {
                        fontSize: 15
                    }
                }],
                yAxes: [{
                    ticks: {
                        fontSize: 20
                    }
                }]
            }
        }
        that.labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        that.series = ['Total Budget', 'Expenditure'];
        that.data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ];

        that.categories = []

        budgetService.getAllCategories()
            .then(function(response) {
                that.categories = response;
            });
        budgetService.getMonthlyBudget(month)
            .then(function(response) {
                that.totalBudget = response.totalBudget;
                that.remainingBudget = response.remainingBudget;
                that.budgetId = response.id;
            });

        that.callMe = function() {
            var categoryWiseExpense = {};
            that.labels2 = [];
            that.data2 = [];
            budgetService.getMonthlyExpense(month)
                .then(function(re) {
                    that.expenses = re;
                    re.forEach(function(element) {
                        var ammount = categoryWiseExpense[element.category] ? categoryWiseExpense[element.category] : 0;
                        ammount = ammount + element.ammount;
                        categoryWiseExpense[element.category] = ammount;
                    }, this);
                    for (var category in categoryWiseExpense) {
                        that.labels2.push(category);
                        that.data2.push(categoryWiseExpense[category]);
                    }
                });
        };

        that.callMe();


        that.toggleExpenseForm = function() {
            that.showExpenseForm = that.showExpenseForm ? false : true;
        }

        that.addExpense = function() {
            if (that.ammount > 0 && that.description != "" && that.selectedCategory) {
                var expenseObj = {
                    "ammount": that.ammount,
                    "description": that.description,
                    "category": that.selectedCategory,
                    "madeOn": new Date(),
                    "month": new Date().getMonth()
                }
                that.remainingBudget = that.remainingBudget - that.ammount;

                var budgetObj = {
                    "totalBudget": that.totalBudget,
                    "remainingBudget": that.remainingBudget,
                    "month": new Date().getMonth()
                }
                var budgetJsonObj = JSON.stringify(budgetObj);
                budgetService.updateBudget(budgetObj, that.budgetId).then(function(re) {});
                var jsonObj = JSON.stringify(expenseObj);
                budgetService.addExpense(jsonObj)
                    .then(function(re) {
                        that.expenses.push(re);

                    });
            }
            that.ammount = 0;
            that.selectedCategory = "";
            that.description = "";
            that.showExpenseForm = false;
            that.callMe();

        }

        that.labels2 = [];
        that.data2 = [];
        that.datasetOverride2 = {
            hoverBackgroundColor: ['#45b7cd', '#ff6384', '#ff8e72'],
            hoverBorderColor: ['#45b7cd', '#ff6384', '#ff8e72']
        };
        budgetService.getCompleteBudget()
            .then(function(re) {
                that.completeBudget = re;
                that.completeBudget.forEach(function(element) {
                    that.data[0][element['month']] = element['totalBudget'];
                    that.data[1][element['month']] = element['totalBudget'] - element['remainingBudget'];
                }, this);
            });
    }
})();