import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { UsersComponent } from './components/users/users.component';
import { CampaignsComponent } from './components/campaigns/campaigns.component';
import { MarkdownViewerComponent } from './components/markdown-viewer/markdown-viewer.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'users', component: UsersComponent },
  { path: 'campaigns', component: CampaignsComponent },
  { 
    path: 'docs/coding-guidelines', 
    component: MarkdownViewerComponent, 
    data: { markdownPath: 'assets/docs/coding_guidelines.md' }
  },
  { 
    path: 'docs/general-guidelines', 
    component: MarkdownViewerComponent, 
    data: { markdownPath: 'assets/docs/general_guidelines.md' }
  },
  { 
    path: 'docs/backend-guidelines', 
    component: MarkdownViewerComponent, 
    data: { markdownPath: 'assets/docs/backend_guidelines.md' }
  },
  { 
    path: 'docs/frontend-guidelines', 
    component: MarkdownViewerComponent, 
    data: { markdownPath: 'assets/docs/frontend_guidelines.md' }
  },
  { path: '**', redirectTo: '' }
];
