// Test script to verify API endpoints
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api';

async function testAPI() {
  console.log('Testing API endpoints...\n');
  
  try {
    // Test health check
    console.log('1. Testing health endpoint...');
    const healthResponse = await axios.get(`${BASE_URL}/health`);
    console.log('✓ Health check passed:', healthResponse.data);
    
    // Test signup
    console.log('\n2. Testing signup endpoint...');
    const signupData = {
      email: 'test@example.com',
      password: 'password123',
      name: 'Test User'
    };
    const signupResponse = await axios.post(`${BASE_URL}/auth/signup`, signupData);
    console.log('✓ Signup successful:', signupResponse.data.user.name);
    
    // Test signin
    console.log('\n3. Testing signin endpoint...');
    const signinData = {
      email: 'test@example.com',
      password: 'password123'
    };
    const signinResponse = await axios.post(`${BASE_URL}/auth/signin`, signinData);
    const token = signinResponse.data.token;
    console.log('✓ Signin successful, token received');
    
    // Test creating a task
    console.log('\n4. Testing create task endpoint...');
    const taskData = {
      title: 'Test Task',
      description: 'This is a test task'
    };
    const createTaskResponse = await axios.post(
      `${BASE_URL}/tasks`,
      taskData,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    const taskId = createTaskResponse.data.id;
    console.log('✓ Task created:', createTaskResponse.data.title);
    
    // Test getting tasks
    console.log('\n5. Testing get tasks endpoint...');
    const getTasksResponse = await axios.get(
      `${BASE_URL}/tasks`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    console.log('✓ Tasks retrieved:', getTasksResponse.data.length);
    
    // Test updating a task
    console.log('\n6. Testing update task endpoint...');
    const updateData = {
      title: 'Updated Test Task',
      completed: true
    };
    const updateTaskResponse = await axios.put(
      `${BASE_URL}/tasks/${taskId}`,
      updateData,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    console.log('✓ Task updated:', updateTaskResponse.data.title);
    
    // Test deleting a task
    console.log('\n7. Testing delete task endpoint...');
    const deleteTaskResponse = await axios.delete(
      `${BASE_URL}/tasks/${taskId}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    console.log('✓ Task deleted');
    
    console.log('\n✓ All API tests passed successfully!');
  } catch (error) {
    console.error('✗ API test failed:', error.response?.data || error.message);
  }
}

testAPI();