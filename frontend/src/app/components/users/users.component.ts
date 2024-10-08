import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { UserService, User } from '../../services/user.service';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatProgressSpinnerModule],
  template: `
    <h1>Users</h1>
    <div *ngIf="loading" class="loading-spinner">
      <mat-spinner></mat-spinner>
    </div>
    <table mat-table [dataSource]="users" class="mat-elevation-z8" *ngIf="!loading">
      <ng-container matColumnDef="username">
        <th mat-header-cell *matHeaderCellDef>Username</th>
        <td mat-cell *matCellDef="let user">{{user.username}}</td>
      </ng-container>
      <ng-container matColumnDef="email">
        <th mat-header-cell *matHeaderCellDef>Email</th>
        <td mat-cell *matCellDef="let user">{{user.email}}</td>
      </ng-container>
      <ng-container matColumnDef="first_name">
        <th mat-header-cell *matHeaderCellDef>First Name</th>
        <td mat-cell *matCellDef="let user">{{user.first_name}}</td>
      </ng-container>
      <ng-container matColumnDef="last_name">
        <th mat-header-cell *matHeaderCellDef>Last Name</th>
        <td mat-cell *matCellDef="let user">{{user.last_name}}</td>
      </ng-container>
      <ng-container matColumnDef="is_active">
        <th mat-header-cell *matHeaderCellDef>Active</th>
        <td mat-cell *matCellDef="let user">{{user.is_active ? 'Yes' : 'No'}}</td>
      </ng-container>

      <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
      <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
    </table>
  `,
  styles: [`
    .loading-spinner {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 200px;
    }
    table {
      width: 100%;
    }
  `]
})
export class UsersComponent implements OnInit {
  users: User[] = [];
  displayedColumns: string[] = ['username', 'email', 'first_name', 'last_name', 'is_active'];
  loading = true;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.getUsers().subscribe({
      next: (users) => {
        this.users = users;
        this.loading = false;
        console.log('Users loaded successfully:', users);
      },
      error: (error) => {
        console.error('Error fetching users:', error);
        if (error.status === 307) {
          console.log('Redirect location:', error.headers.get('Location'));
        }
        this.loading = false;
        // Display an error message to the user
        alert('An error occurred while fetching users. Please try again later.');
      }
    });
  }
}
