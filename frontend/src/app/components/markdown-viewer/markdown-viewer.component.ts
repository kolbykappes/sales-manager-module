import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { marked } from 'marked';

@Component({
  selector: 'app-markdown-viewer',
  standalone: true,
  imports: [CommonModule, MatProgressSpinnerModule],
  template: `
    <div *ngIf="loading" class="loading-spinner">
      <mat-spinner></mat-spinner>
    </div>
    <div *ngIf="!loading" [innerHTML]="markdownContent"></div>
  `,
  styles: [`
    .loading-spinner {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 200px;
    }
  `]
})
export class MarkdownViewerComponent implements OnInit {
  markdownContent: string = '';
  loading: boolean = true;

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit() {
    this.route.data.subscribe(data => {
      const markdownPath = data['markdownPath'];
      this.http.get(markdownPath, { responseType: 'text' }).subscribe({
        next: (content) => {
          this.markdownContent = marked(content);
          this.loading = false;
        },
        error: (error) => {
          console.error('Error loading markdown file:', error);
          this.markdownContent = 'Error loading content.';
          this.loading = false;
        }
      });
    });
  }
}
