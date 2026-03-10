import './App.css';
import '@mantine/core/styles.css';
import { MantineProvider, Center, Button } from '@mantine/core';

export default function App() {
	return (
		<MantineProvider>
			<Center style={{ minHeight: '100vh' }}>
				<Button>Click me</Button>
			</Center>
		</MantineProvider>
	);
}
