const AppUnit = {
    data() {
        return {
            id_unit: {}, // id текущего юнита
            currentUnitData: {}, // данные о текущем юните
            currentObj: {}, // Objective текущего года в MYP
            selectedObj: [], // выбранные галочкой Objective
            criteria: {}, // критерии текущей предметной области
            showButtonSave: false,
            showButtonChange: true,
        }
    },
    computed: {},
    methods: {
        async getUnit() {
            // Получение данных из переменной Django (номер текущего юнита)
            this.id_unit = JSON.parse(document.getElementById('dataUnit').textContent);
            console.log("Данные: ", this.id_unit);
            // Запрос на информацию по текущему юниту
            this.currentUnitData = await axios.get('/api/unit/' + this.id_unit)
                .then(function (response) {
                    console.log('Информация о юните: ', response.data);
                    return response.data;
                });
            // Заполнение массива выбранных галочек из списка Objective 
            // в соответствии с Objective текушего юнита
            let obj = new Array()
            this.currentUnitData.objective.forEach(function (item) { obj.push(item.id) });
            this.selectedObj = obj;
            // Запрос на информацию по списку критериев
            this.criteria = await axios.get('/api/criteria')
                .then(function (response) {
                    return response.data
                })
            console.log('Критерии: ', this.criteria)
            this.currentObj = await axios.get('/api/objective', {
                params: {
                    'year': Number(this.currentUnitData.year_ib.year_ib)
                }
            }).then(function (response) {
                currentObjA = response.data.filter(function (obj) {
                    return obj.criteria.letter == 'A';
                });
                currentObjB = response.data.filter(function (obj) {
                    return obj.criteria.letter == 'B';
                });
                currentObjC = response.data.filter(function (obj) {
                    return obj.criteria.letter == 'C';
                });
                currentObjD = response.data.filter(function (obj) {
                    return obj.criteria.letter == 'D';
                });
                return { 'A': currentObjA, 'B': currentObjB, 'C': currentObjC, 'D': currentObjD }
            })
            console.log('Информация об Objectives:', this.currentObj)
        },
        changeClick() {
            this.showButtonSave = !this.showButtonSave;
            this.showButtonChange = !this.showButtonChange;
        },
        cancelClick() {
            location.reload();
        },
        saveClick() {
            this.showButtonSave = !this.showButtonSave;
            this.showButtonChange = !this.showButtonChange;

            let csrftoken = Cookies.get("csrftoken");
            let headers = {
                "X-CSRFToken": csrftoken,
                "content-type": "application/json"
            };
            let data = {
                'obj': this.selectedObj,
            }
            axios.put('/api/unit/' + this.id_unit, data, { headers })
                .then(response => {
                    console.log(response);
                    location.reload();
                    // window.location = ""
                })
                .catch(error => {
                    console.log(error);
                });
        },
        // проверка добавленных Objective в Unit
        objectivesInUnit(obj) {
            for (let i = 0; i < this.currentUnitData.objective.length; i++) {
                if (this.currentUnitData.objective[i].id == obj) {
                    return true
                }
            }
            return false
        },
    },
    mounted() {
        this.getUnit(this.currentObj);
    }
};

const AppStudent = {
    data() {
        return {
            id_group: {},
            id_unit: null,
            studentGroup: [],
            group: {},
            selectedStudent: [],
            csrftoken: '',
        }
    },
    computed: {

    },
    methods: {
        async getGroupInfo() {
            this.id_unit = JSON.parse(document.getElementById('dataUnit').textContent);
            this.id_group = JSON.parse(document.getElementById('dataGroup').textContent);
            console.log("Выбранный класс: ", this.id_group);
            this.group = await axios.get('/api/group', {
                params: {
                    'group': this.id_group,
                }
            }).then(function (response) {
                year = response.data[0];
                return {
                    grade: year.year.grade_rus,
                    letter: year.letter
                };
            })
        },

        async getStudent() {
            this.studentGroup = await axios.get('/api/student', {
                params: {
                    'group': this.id_group,
                }
            }).then(function (response) {
                console.log('Информация о студентах: ', response.data);
                return response.data;
            })
        },

        addStudent() {
            let csrftoken = Cookies.get("csrftoken");
            let headers = {
                "X-CSRFToken": csrftoken,
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            };
            let data = {
                student: this.selectedStudent,
                unit: this.id_unit,
            }
            axios.post("/sumassess/students/", Qs.stringify(data), { headers }).then(response => {
                location.reload();
                return response
            })
                .catch(function (error) { });
        },

        addedStudent(stud) {
            for (let i = 0; i < stud.length; i++) {
                if (this.id_unit == stud[i].unit) {
                    return true
                }
            }
            return false
        },
        goToBack() {
            location.href="/sumassess/";
        }

    },
    mounted() {
        this.getGroupInfo()
    }
};

Vue.createApp(AppUnit).mount("#appunit")
Vue.createApp(AppStudent).mount("#appstudent")