import React, {useState} from 'react';
import {Route, Routes} from 'react-router-dom';
import {HomePage} from './pages/HomePage';
import {DashboardPage} from './pages/DashboardPage';
import {MenuPage} from './pages/MenuPage';
import {CategoryPage} from './pages/CategoryPage';
import {GuildPrefixPage} from "./pages/ConfigurationPages/GuildPrefixPage";
import {WelcomeMessagePage} from "./pages/ConfigurationPages/WelcomeMessagePage";
import {GuildDashboardPage} from "./pages/GuildDashboardPage";
import {ServerListPage} from "./pages/ServerListPage";
import {GuildContext} from "./utils/contexts/GuildContext";


function App() {
    const [guildId, setGuildId] = useState('');
    const updateGuildId = (id: string) => setGuildId(id)
    return (
        <GuildContext.Provider value={{
            guildId, updateGuildId: () => {
            }
        }}>
            <Routes>
                <Route path="/" element={<HomePage/>}/>
                <Route path="/Dashboard" element={<DashboardPage/>}/>
                <Route path="/Menu" element={<MenuPage/>}/>
                <Route path={"/Server"} element={<ServerListPage/>}/>
                <Route path={'/Guild/Dashboard'} element={<GuildDashboardPage/>}/>
                <Route path="/Guild/Category" element={<CategoryPage/>}/>
                <Route path="/Guild/Update-Prefix" element={<GuildPrefixPage/>}/>
                <Route path="/Guild/Welcome-Message" element={<WelcomeMessagePage/>}/>
            </Routes>
        </GuildContext.Provider>
    );
}

export default App;
