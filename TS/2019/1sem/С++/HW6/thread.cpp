#include <thread>
#include <iostream>
#include <atomic>

using namespace std;
atomic<int> flag(0);

void thread_1() {
	int i = 0;
	while (i < 500000) {
		if (flag == 0) {
			cout << "ping" << endl;
			++i;
			flag = 1;
		}
	}
}
void thread_2() {
	int i = 0;
	while (i < 500000) {
		if (flag == 1) {
			cout << "pong" << endl;
			++i;
			flag = 0;
		}
	}
}

int main() {
	thread t1(thread_1), t2(thread_2);
	t1.join();
	t2.join();
	return 0;
}
