
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: 'login', component: () => import('pages/Login.vue') },
      //{ path: 'register', component: () => import('pages/Register.vue') },
      { path: 'wells', component: () => import('pages/WellList.vue') },
      { path: 'wells/:id', component: () => import('pages/WellDetail.vue') },
      { path: 'staffs', component: () => import('pages/Staff.vue') },
      { path: 'staffs/:id', component: () => import('pages/NewStaff.vue') },
      { path: 'soil', component: () => import('pages/MusterSoilList.vue') },
      { path: 'soil/:id', component: () => import('pages/MusterSoilDetail.vue') },
      { path: 'farms', component: () => import('pages/FarmList.vue') },
      { path: 'reports', component: () => import('pages/Reports.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
