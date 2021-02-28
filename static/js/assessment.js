const AssessmentUnit = {
    data() {
        return {
            title: "Оценивание студента",
            selectedAssessmentStudentID: {},
            correctYearID: {},
            correctUnitID: {},
            currentLevel: [],
            currentObj: [],
            criteria: [],
            selectedLevel: {},
            correctGroupID: {},
            markIB: { 'A': 0, 'B': 0, 'C': 0, 'D': 0, },
            idx: 0,
        }
    },
    computed: {

    },
    methods: {
        async getAssessmentStudent() {
            this.selectedAssessmentStudentID = JSON.parse(document.getElementById('dataAssessStudent').textContent);
            this.correctYearID = JSON.parse(document.getElementById('dataYear').textContent);
            this.correctUnitID = JSON.parse(document.getElementById('dataUnit').textContent);
            this.correctGroupID = JSON.parse(document.getElementById('dataGroup').textContent);
            // Получение выбранных level текущего ученика в журнале юнита
            this.selectedLevel = await axios.get('/api/assessmentunit/' + this.selectedAssessmentStudentID)
                .then(function (response) {
                    let objUnit = response.data.unit.objective
                    let levelAssess = response.data.level
                    let selectedLevel = {}
                    objUnit.forEach(function (obj) {
                        selectedLevel[obj.id] = { 'criterion': obj.criteria.letter, 'point': 0 }
                        levelAssess.forEach(function (level) {
                            if (obj.id == level.objective.id) {
                                selectedLevel[obj.id] = { 'id': level.id, 'criterion': level.objective.criteria.letter, 'point': level.point }
                            }
                        });
                    });
                    return selectedLevel
                }).then((data) => {
                    return data;
                });
            this.markIB = this.calculateMark();
            console.log('Загруженные Levels', this.selectedLevel)
            $('#myTab li:first-child a').tab('show')
        },
        async getLevelYear() {
            // Запрос на получение всех уровней выбранного года
            this.currentLevel = await axios.get('/api/levels/', {
                params: {
                    'year': this.correctYearID,
                    'unit': this.correctUnitID,
                }
            }).then(function (response) {
                console.log('Выбранные levels: ', response.data);
                return response.data;
            });
        },

        async getObjective() {
            this.currentObj = await axios.get('/api/objective', {
                params: {
                    'year': this.correctYearID,
                    'unit': this.correctUnitID,
                }
            }).then(function (response) {
                return response.data
            });
            console.log('Информация об Objectives:', this.currentObj)
        },

        async getCriteria() {
            this.criteria = await axios.get('/api/criteria')
                .then(function (response) {
                    return response.data
                });
            console.log('Информация о критериях:', this.criteria);
        },

        objLevel(cr_letter, st_letter) {
            return this.currentLevel.filter(function (level) {
                return level.objective.criteria.letter == cr_letter && level.objective.strand.letter == st_letter
            });
        },

        objCriteria(letter) {
            return this.currentObj.filter(function (obj) {
                return obj.criteria.letter == letter
            });
        },

        isShow(id) {
            if (id == 0) {
                return false
            } else {
                return true
            }
        },

        calculateMark() {
            maxPoints = { 'A': 0, 'B': 0, 'C': 0, 'D': 0, };
            currentPoints = { 'A': 0, 'B': 0, 'C': 0, 'D': 0, };
            markIB = { 'A': 0, 'B': 0, 'C': 0, 'D': 0, };
            for (let obj in this.selectedLevel) {
                maxPoints[this.selectedLevel[obj].criterion] += 4
                currentPoints[this.selectedLevel[obj].criterion] += this.selectedLevel[obj].point
            }
            for (let letter in currentPoints) {
                markIB[letter] = Math.round((currentPoints[letter] * 8) / maxPoints[letter]) || 0
            }
            // console.log('Полученные баллы', currentPoints)
            // console.log('Возможные баллы', maxPoints)
            // console.log('IB баллы', markIB)
            return markIB
        },

        // Сохранение выбранных Level в записи в таблице AssessmenrUnit
        saveClick() {
            let levels = []
            for (key in this.selectedLevel) {
                levels.push({ "id": this.selectedLevel[key].id })
            }
            this.markIB = this.calculateMark();
            let csrftoken = Cookies.get("csrftoken");
            let headers = {
                "X-CSRFToken": csrftoken,
                "content-type": "application/json"
            };
            let data = {
                'level': levels,
                'mark_a': this.markIB['A'],
                'mark_b': this.markIB['B'],
                'mark_c': this.markIB['C'],
                'mark_d': this.markIB['D'],
            }
            // PUT-запрос на добавление Level к текушему студенту в журнале юнита
            axios.put('/api/assessmentunit/' + this.selectedAssessmentStudentID, data, { headers })
                .then(response => {
                    console.log(response);
                    location.reload();
                    // location.href="/sumassess/students/?unit="+this.correctUnitID+"&class="+this.correctGroupID;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        goToBack() {
            location.href="/sumassess/students/?unit="+this.correctUnitID+"&class="+this.correctGroupID;
        }

    },
    mounted() {
        this.getAssessmentStudent();
        this.getLevelYear();
        this.getObjective();
        this.getCriteria();
        
    }
};

Vue.createApp(AssessmentUnit).mount("#assessment")