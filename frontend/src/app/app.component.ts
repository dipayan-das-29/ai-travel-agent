import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment'; // Import environment config

export interface LogEntry {
  timestamp: string;
  message: string;
  type: 'info' | 'tool' | 'success' | 'error';
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'travel-agent-ui';

  userPrompt: string = 'Plan a 3-day budget trip to Kyoto for 1 person including flight and hotel costs.';
  isLoading: boolean = false;
  itineraryOutput: string = '';
  logs: LogEntry[] = [];

  constructor(private http: HttpClient) {}

  generateItinerary(): void {
    if (!this.userPrompt.trim()) return;

    this.isLoading = true;
    this.itineraryOutput = '';
    this.logs = [];

    this.addLog('Received user travel prompt', 'info');
    this.addLog(`Sending request to API target: ${environment.apiBaseUrl}`, 'info');

    // 🔌 Dynamically construct endpoint using environment configuration
    const endpoint = `${environment.apiBaseUrl}/api/plan`;

    this.http.post<{ result: string }>(endpoint, { prompt: this.userPrompt })
      .subscribe({
        next: (res) => {
          this.addLog('Received final itinerary from agent', 'success');
          this.itineraryOutput = res.result;
          this.isLoading = false;
        },
        error: (err) => {
          this.addLog(`Error connecting to ${endpoint}: ${err.message || 'Server offline'}`, 'error');
          this.isLoading = false;
        }
      });
  }

  private addLog(message: string, type: 'info' | 'tool' | 'success' | 'error' = 'info'): void {
    const timestamp = new Date().toLocaleTimeString();
    this.logs.push({ timestamp, message, type });
  }
}