import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { UsersComponent } from './components/users/users.component';
import { CampaignsComponent } from './components/campaigns/campaigns.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'users', component: UsersComponent },
  { path: 'campaigns', component: CampaignsComponent },
  { path: '**', redirectTo: '' }
];
