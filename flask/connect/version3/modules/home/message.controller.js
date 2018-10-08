(function() {
    angular.module('Home').controller('MessageController', MessageController);
    MessageController.$inject = ['MessageService'];

    function MessageController(MessageService) {
        var vm = this;
        MessageService.SetCredentials();
        vm.peopleList = [];
        vm.selectedPerson = '';
        MessageService.GetPeople().then(function(response) {
            vm.peopleList = response;
            if (vm.peopleList[0]) {
                vm.getConversation(vm.peopleList[0])
            }
        });

        vm.getConversation = function(person) {
            vm.message = "";
            vm.selectedPerson = person;
            MessageService.GetMessages(person).then(function(response) {
                vm.conversation = response;
            });
        }

        vm.sendMessage = function(message, person) {
            vm.message = "";
            MessageService.SendMessage(message, person).then(function(response) {
                MessageService.GetMessages(person).then(function(response) {
                    vm.conversation = response;
                });
            });
        }
    }
})();