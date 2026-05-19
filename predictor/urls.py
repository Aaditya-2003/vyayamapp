# predictor/urls.py
from django.urls import path
from .views import live_pose, pose_correction_api, pose_grid, pose_instructions

urlpatterns = [
  
     path('', pose_grid, name='pose_grid'),
    path('pose/<int:pose_id>/', pose_instructions, name='pose_instructions'),
    path('live_pose/<int:pose_id>/', live_pose, name='live_pose'),
    # API and other routes as needed
    path('api/correct_pose/', pose_correction_api, name='pose_correction_api'),
]
