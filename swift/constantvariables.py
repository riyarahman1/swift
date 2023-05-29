APPURL = ""
APPFOLDERNAME = "swift"
PAGINATION_PERPAGE = 3
UAE_TIMEZONE = 'Asia/Dubai'

PERFORMANCE_MAIN_MENU = 14
KPI_CATEGORY_MENU = 17
KPI_GOAL_MENU = 18
KPI_GOAL_SETTING_MENU = 25
KPI_EMPLOYEE_MENU = 19

REQUESTS_MAIN_MENU = 61
LEAVE_REQUESTS_MENU = 33

APPRAISAL_CATEGORY_MENU = 21
APPRAISAL_POINT_MENU = 22
APPRAISAL_EMPLOYEE_MENU = 23

APPRAISAL_RATING = 2
KPI_PERCENTAGE = 70
RATING_PERCENTAGE = 30

APPRAISAL_PENDING = 1
APPRAISAL_WAITING_EMPLOYEE_EVALUATION = 2
APPRAISAL_WAITING_LEVEL_1_EVALUATION = 3
APPRAISAL_WAITING_LEVEL_2_EVALUATION = 4
APPRAISAL_WAITING_LEVEL_3_EVALUATION = 5
APPRAISAL_WAITING_HR_REVIEW = 6
APPRAISAL_WAITING_HOD_REVIEW = 7
APPRAISAL_WAITING_EMPLOYEE_APPROVAL = 8
APPRAISAL_WAITING_HR_APPROVAL = 9
APPRAISAL_WAITING_SUPERVISOR_APPROVED = 10

PROBATION_PENDING = 1
PROBATION_WAITING_HOD_APPROVAL = 2
PROBATION_WAITING_EMPLOYEE_APPROVAL = 3
PROBATION_WAITING_HR_APPROVAL = 4
PROBATION_WAITING_MD_APPROVAL = 5
#PROBATION_HR_APPROVED = 5
PROBATION_MD_APPROVED = 6
PROBATION_REJECTED = 7

FROM_EMAIL = 'no-reply@hisense-hiconnect.com'

HR_ROLE_USER = 17
IT_ADMIN_USER = 22
ADMIN_ROLE_USER = 15

permission_list = {
    'add_group':'Create',
    'change_group':'Edit',
    'delete_group':'Delete',
    'view_group':'View',
    'add_designation':'Create',
    'change_designation':'Edit',
    'delete_designation':'Delete',
    'view_designation':'View',
    'add_flightticket':'Create',
    'change_flightticket':'Edit',
    'view_flightticket':'View',
    'delete_flightticket':'Delete',
    'add_salarytransferletter':'Create',
    'view_salarytransferletter':'View',
    'view_events':'View',
}

sub_permission_list = {
    'add_group':'Create',
    'change_group':'Edit',
    'delete_group':'Delete',
    'view_group':'View',
    
    'add_designation':'Create',
    'change_designation':'Edit',
    'delete_designation':'Delete',
    'view_designation':'View',

    'add_department':'Create',
    'change_department':'Edit',
    'delete_department':'Delete',
    'view_department':'View',

    'add_user':'Create',
    'change_user':'Edit',
    'delete_user':'Delete',
    'view_user':'View',

    'add_jobtypes':'Create',
    'change_jobtypes':'Edit',
    'delete_jobtypes':'Delete',
    'view_jobtypes':'View',

    'add_user_status':'Create',
    'change_user_status':'Edit',
    'delete_user_status':'Delete',
    'view_user_status':'View',

    'add_branch':'Create',
    'change_branch':'Edit',
    'delete_branch':'Delete',
    'view_branch':'View',

    
    'add_employeevisastatus':'Create',
    'change_employeevisastatus':'Edit',
    'delete_employeevisastatus':'Delete',
    'view_employeevisastatus':'View',

    'add_hod':'Create',
    'change_hod':'Edit',
    'delete_hod':'Delete',
    'view_hod':'View',

    'add_kpiyear':'Create',
    'change_kpiyear':'Edit',
    'delete_kpiyear':'Delete',
    'view_kpiyear':'View',

    'add_userstatus':'Create',
    'change_userstatus':'Edit',
    'delete_userstatus':'Delete',
    'view_userstatus':'View',
    
    'add_leavetype':'Create',
    'change_leavetype':'Edit',
    'delete_leavetype':'Delete',
    'view_leavetype':'View',

    'add_kpiaction': 'Create',
    'change_kpiaction':'Edit',
    'delete_kpiaction':'Delete',
    'view_kpiaction':'View',

    'add_kpiactionpermission': 'Create',
    'change_kpiactionpermission':'Edit',
    'delete_kpiactionpermission':'Delete',
    'view_kpiactionpermission':'View',

    'add_userappraisalevaluation':'Evaluate',

    'view_kpiuseractual':'View',

    'add_leaveyear':'Create',
    'change_leaveyear':'Edit',
    'delete_leaveyear':'Delete',
    'view_leaveyear':'View',

    'add_leavesetting':'Create',
    'change_leavesetting':'Edit',
    'delete_leavesetting':'Delete',
    'view_leavesetting':'View',

    'add_leaverequest':'Create',
    'change_leaverequest':'Approve/Reject',
    'view_leaverequest':'View',

    'add_leavepermission':'Create',
    'change_leavepermission':'Edit',
    'delete_leavepermission':'Delete',
    'view_leavepermission':'View',

    'add_useryearleave':'Create',
    'change_useryearleave':'Edit',
    'delete_useryearleave':'Delete',
    'view_useryearleave':'View',

    'change_userappraisalforms':'Approve',

    'add_userappraisalgrade':'Approve',

    'add_kpiusertimeperiod':'Create',
    'change_kpiusertimeperiod':'Edit',
    'delete_kpiusertimeperiod':'Delete',
    'view_kpiusertimeperiod':'View',

    'add_kpitimeperiod':'Create',
    'change_kpitimeperiod':'Edit',
    'delete_kpitimeperiod':'Delete',
    'view_kpitimeperiod':'View',

    'add_holidays':'Create',
    'change_holidays':'Edit',
    'delete_holidays':'Delete',
    'view_holidays':'View',

    'view_kpiusertarget':'View',
    'change_employeeeiddetails':'Change',
    

    #my ticket
    'add_employeeskills':'Create',
    'change_employeeskills':'Edit',
    'delete_employeeskills':'Delete',
    'view_employeeskills':'View',
    
    'change_trainingcourse':'Edit',
    'delete_trainingcourse':'Delete',
    'view_trainingcourse':'View',

    'add_coursecontenthistory':'Create',
    'add_relatedcourse': 'Create',

    'add_leavepolicy':'Create',
    'change_leavepolicy':'Edit',
    'delete_leavepolicy':'Delete',
    'view_leavepolicy':'View',

    'add_sallarycertificatesrequests':'View/Send Request',
    # 'change_sallarycertificatesrequests':'Edit',
    # 'view_sallarycertificatesrequests':'View',
    # 'delete_sallarycertificatesrequests':'Delete',

    # 'add_salarytransferletter':'Create',
    # 'change_salarytransferletter':'Edit',
    'view_salarytransferletter':'Approve/Reject',
    # 'delete_salarytransferletter':'Delete',

    'add_policyprocedure':'Create',
    'view_policyprocedure':'View',

    'add_appraisalpoint':'Create',
    'change_appraisalpoint':'Edit',
    'view_appraisalpoint':'View',
    'delete_appraisalpoint':'Delete',
    
    'add_inusrancepolicy':'Create',
    'change_inusrancepolicy':'Edit',
    'view_inusrancepolicy':'View',
    'delete_inusrancepolicy':'Delete',

    #medical insurance
    'add_medicalinsurancedocuments':'Create',
    'change_medicalinsurancedocuments':'Edit',
    'view_medicalinsurancedocuments':'View',
    'delete_medicalinsurancedocuments':'Delete',

    #'add_userappraisalevaluationtime':'Create',
    'change_userappraisalevaluationtime':'Set Date',
    #'view_userappraisalevaluationtime':'View',
    #'delete_userappraisalevaluationtime':'Delete',

    'add_careers':'Create',
    'change_careers':'Edit',
    'view_careers':'View',
    'delete_careers':'Delete',

    'add_jobdescription':'Create',
    'change_jobdescription':'Edit',
    'view_jobdescription':'View',
    'delete_jobdescription':'Delete',

    'add_corporatevideo':'Create',
    'change_corporatevideo':'Edit',
    'view_corporatevideo':'View',
    'delete_corporatevideo':'Delete',

    'view_coursecontent':'View',

    #'add_useradminchat':'Create',
    'change_useradminchat':'Approve or Reject',
    # 'view_useradminchat':'View',
    # 'delete_useradminchat':'Delete',

    'add_jobapplication':'Create',
    'change_jobapplication':'Edit',
    'view_jobapplication':'View',
    'delete_jobapplication':'Delete',


    'add_experienceyears':'Create',
    'change_experienceyears':'Edit',
    'view_experienceyears':'View',
    'delete_experienceyears':'Delete',

    'add_events':'Create',
    'change_events':'Edit',
    'view_events':'View',
    'delete_events':'Delete',

    'add_measurementtype':'Create',
    'change_measurementtype':'Edit',
    'view_measurementtype':'View',
    'delete_measurementtype':'Delete',

    'change_trainingrequests':'Edit / Cancel',
    'view_trainingrequests':'View',

    'add_flightticket':'Create',
    'change_flightticket':'Edit',
    'view_flightticket':'View',
    'delete_flightticket':'Delete',

    'change_trainingrequeststatus':'Approve / Reject',
    'view_trainingrequeststatus':'View',

    'add_payrollupload':'Create',
    'change_payrollupload':'Edit',
    'view_payrollupload':'View',
    'delete_payrollupload':'Delete',

    'view_payrollmaster':'View',
    'view_payrolldetail':'View',

    'add_splashscreen':'Create',
    'change_splashscreen':'Edit',
    'view_splashscreen':'View',
    'delete_splashscreen':'Delete',

    'add_leaveadjustment':'Create',
    'change_leaveadjustment':'Edit',
    'view_leaveadjustment':'View',
    'delete_leaveadjustment':'Delete',

    'add_experienceLevel':'Create',
    'change_experienceLevel':'Edit',
    'view_experienceLevel':'View',
    'delete_experienceLevel':'Delete',

    # 'add_attendancelog':'Create',
    # 'change_attendancelog':'Edit',
    'view_attendancelog':'View/Send Request',
    # 'delete_attendancelog':'Delete',

    # 'add_attendancerequests':'Create',
    'change_attendancerequests':'Approve/Reject',
    # 'view_attendancerequests':'View',
    # 'delete_attendancerequests':'Delete',

    # 'add_attendancerequestslog':'Create',
    # 'change_attendancerequestslog':'Edit',
    'view_attendancerequestslog':'View',
    # 'delete_attendancerequestslog':'Delete',

    'add_probationpoint':'Create',
    'change_probationpoint':'Edit',
    'view_probationpoint':'View',
    'delete_probationpoint':'Delete',

    'add_leaveadjustment':'Create',
    'change_leaveadjustment':'Edit',
    'view_leaveadjustment':'View',
    'delete_leaveadjustment':'Delete',

    'add_probationform':'Evaluate',
    'add_probationrating':'Evaluate',
    'add_profile':'Create',

    'view_employeeaddress':'View',

    'add_experiencelevel':'Create',
    'change_experiencelevel':'Edit',
    'view_experiencelevel':'View',
    'delete_experiencelevel':'Delete',

    'change_leavestatuslog':'Edit / Cancel',
    'view_leavestatuslog':'View',

    'add_userpolicyleave':'Create',
    }
