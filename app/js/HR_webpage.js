const addressCourse = "3.131.65.207:5144"
const addressUser = "3.131.65.207:5744"
const addressClass = "3.131.65.207:5044"
const addressInstructor = "3.131.65.207:5244"

const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

const today = new Date();

const quiz_app = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {

          headers_class: [
            {
              text: 'Class ID',
              align: 'start',
              value: 'Class_ID',
            },
            { text: 'Class Name', value: 'Class_Name' },
            { text: 'Class Details', value: 'Class_Details' },
            { text: 'Size', value: 'Size' },
            { text: 'Current_Size', value: 'Current_Size' },
            { text: 'Instructor', value: 'Instructor' },
            { text: 'Start_Time', value: 'Start_Time' },
            { text: 'End_Time', value: 'End_Time' },
            { text: 'Students', value: 'Students' },
            { text: 'Actions', value: 'actions' },
          ],

          headers_instructor: [
            {
                text: 'Instructor_ID',
                align: 'start',
                value: 'Instructor_ID',
              },
              { text: 'Actual Name', value: 'Actual_Name' },
              { text: 'Username', value: 'Username' },
              { text: 'Actions', value: 'actions' },

            ],
        
        class_details:[],
        instructor_list:[],
        class_display: true,
        instructor_display:false,

    },

    created(){    
        this.initalise_all_class()
    }, 
    computed: {

    },
    methods: {
        
        initalise_all_class: function(){
            placehold_array_4 = Array()
            axios.get(`http://${addressClass}/spm/class`)
            .then(function (response) {
                
                class_array = response.data.data.class
                console.log(class_array)
                for (let index = 0; index < class_array.length; index++) {
                    class_details = class_array[index]
                    date_placeholder = {
                        Class_ID:class_details.Class_ID,
                        Class_Name:class_details.Class_Name,
                        Class_Details:class_details.Class_Details,
                        Current_Size:class_details.Current_Size,
                        Size: class_details.Size,
                        Instructor: class_details.Instructor_ID,
                        Start_Time: class_details.Start_Time,
                        End_Time: class_details.End_Time,
                        Sections: class_details.Sections,
                        Students: class_details.Students,
                        Course_ID: class_details.Course_ID,
                    }
                    placehold_array_4.push(date_placeholder)
                }                
            })
            .catch( function (error) {
                console.log(error)
            })

            this.class_details = placehold_array_4
        },

        assign_instructor: function(stuff){
            this.instructor_display = true
            this.class_display = false
            console.log(stuff)
            placehold_array = Array()
            axios.get(`http://${addressInstructor}/spm/instructor`)
            .then(function (response) {
                
                instructor_array = response.data.data.instructor
                console.log(instructor_array)
                for (let index = 0; index < instructor_array.length; index++) {
                    instructor_details = instructor_array[index]
                    instructor_placeholder = {
                        Instructor_ID:instructor_details.Instructor_ID,
                        Actual_Name:instructor_details.Actual_Name,
                        Username:instructor_details.Username,
                        Class_ID:stuff.Class_ID
                    }
                    placehold_array.push(instructor_placeholder)
                }                
            })
            .catch( function (error) {
                console.log(error)
            })

            this.instructor_list = placehold_array
        },

        choose_this_instructor: function(stuff){
            this.instructor_display = true
            this.class_display = false
            console.log(stuff)
            placehold_array = Array()

            post_object = {
                Instructor_ID:stuff.Instructor_ID
            }

            axios.post(`http://${addressClass}/class/` + stuff.Class_ID + `/update`,post_object)
            .then(function (response) {
                alert("Update Successful")         
            })
            .catch( function (error) {
                console.log(error)
            })

        },

        

    }
})
