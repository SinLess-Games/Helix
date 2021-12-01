// Imports and Modules for C#
using System;
using MySql.Data.MySqlClient; // Mysql libarary 
using System.IO;
using System.Threading.Tasks;

public string ex;

public string Ex { get => ex; set => ex = value; }

public class err_log()
{
    public static async Task ExampleAsync()
    {
        return await File.err_log("error" + DateTime.Now.ToFileTime() + ".log", Ex);
    }
};

class DBConnect
{
    private MySqlConnection connection1;
    private MySqlConnection connection2;
    private MySqlConnection connection3;
    private string server;
    private string database1;
    private string database2;
    private string database3;
    private string uid;
    private string password;

    //Constructor
    public DBConnect()
    {
        Initialize();
    }

    //Initialize values
    private void Conection1()
    {
        Console.WriteLine("Building conection 1 Info....")
        server = "localhost:3306";
        database1 = "helix_stats";
        uid = "root";
        password = "";
        string connectionString;
        connectionString = "SERVER=" + server + ";" + "DATABASE=" +
        database + ";" + "UID=" + uid + ";" + "PASSWORD=" + password + ";";
        Console.Write("Conection 1 Built....")
        System.Threading.Thread.Sleep(3000);
        Console.Write("Perparing to conect....")

        connection1 = new MySqlConnection(connectionString);
    }

    //open connection1 to database "helix_stats"
    private bool OpenConnection1()
    {
        try
        {
            Console.WriteLine($"Connecting to Database {database1}....")
            connection1.Open();
            return true;
        }
        catch (MySqlException ex)
        {
            //When handling errors, you can your application's response based 
            //on the error number.
            //The two most common error numbers when connecting are as follows:
            //0: Cannot connect to server.
            //1045: Invalid user name and/or password.
            switch (ex.Number)
            {
                case 0:
                    MessageBox.Show("Cannot connect to server.  Contact administrator");
                    break;

                case 1045:
                    MessageBox.Show("Invalid username/password, please try again");
                    break;
            }
            return false;
        }
    }
    private void conection1_connect()
    {
        if OpenConection1 == true
            Console.WriteLine()
            Console.WriteLine($"Conected to {database1} DataBase.")
        else
            err_log();
            Console.WriteLine("An error orrcured, View ")
    }

    //Initialize values
    private void Conection2()
    {
        Console.Write("Building conection 2 Info....")
        server = "localhost:3306";
        database = "web_permissions";
        uid = "root";
        password = "";
        string connectionString;
        connectionString = "SERVER=" + server + ";" + "DATABASE=" +
        database + ";" + "UID=" + uid + ";" + "PASSWORD=" + password + ";";
        Console.Write("Conection 2 Built....")
        System.Threading.Thread.Sleep(3000);
        Console.Write("Perparing to conect....")

        connection2 = new MySqlConnection(connectionString);
    }
    //Initialize values
    private void Conection3()
    {
        Console.Write("Building conection 3 Info....")
        server = "localhost:3306";
        database = "ai_train_dataset";
        uid = "root";
        password = "";
        string connectionString;
        connectionString = "SERVER=" + server + ";" + "DATABASE=" +
        database + ";" + "UID=" + uid + ";" + "PASSWORD=" + password + ";";
        Console.Write("Conection 3 Built....")
        System.Threading.Thread.Sleep(3000);
        Console.Write("Perparing to conect....")

        connection1 = new MySqlConnection(connectionString);
    }

    //open connection to database
    private bool OpenConnection()
    {
        try
        {
            connection.Open();
            return true;
        }
        catch (MySqlException ex)
        {
            //When handling errors, you can your application's response based 
            //on the error number.
            //The two most common error numbers when connecting are as follows:
            //0: Cannot connect to server.
            //1045: Invalid user name and/or password.
            switch (ex.Number)
            {
                case 0:
                    MessageBox.Show("Cannot connect to server.  Contact administrator");
                    break;

                case 1045:
                    MessageBox.Show("Invalid username/password, please try again");
                    break;
            }
            return false;
        }
    }

    //Close connection
    private bool CloseConnection()
    {
        try
        {
            connection.Close();
            return true;
        }
        catch (MySqlException ex)
        {
            MessageBox.Show(ex.Message);
            return false;
        }
    }

    //Insert statement
    public void Insert()
    {
        string query = "INSERT INTO tableinfo (name, age) VALUES('John Smith', '33')";

        //open connection
        if (this.OpenConnection() == true)
        {
            //create command and assign the query and connection from the constructor
            MySqlCommand cmd = new MySqlCommand(query, connection);

            //Execute command
            cmd.ExecuteNonQuery();

            //close connection
            this.CloseConnection();
        }
    }

    //Update statement
    public void Update()
    {
        tring query = "UPDATE tableinfo SET name='Joe', age='22' WHERE name='John Smith'";

        //Open connection
        if (this.OpenConnection() == true)
        {
            //create mysql command
            MySqlCommand cmd = new MySqlCommand();
            //Assign the query using CommandText
            cmd.CommandText = query;
            //Assign the connection using Connection
            cmd.Connection = connection;

            //Execute query
            cmd.ExecuteNonQuery();

            //close connection
            this.CloseConnection();
        }
    }

    //Delete statement
    public void Delete()
    {
        string query = "DELETE FROM tableinfo WHERE name='John Smith'";

        if (this.OpenConnection() == true)
        {
            MySqlCommand cmd = new MySqlCommand(query, connection);
            cmd.ExecuteNonQuery();
            this.CloseConnection();
        }
    }

    //Select statement
    public List<string>[] Select()
    {
        string query = "SELECT * FROM tableinfo";

        //Create a list to store the result
        List<string>[] list = new List<string>[3];
        list[0] = new List<string>();
        list[1] = new List<string>();
        list[2] = new List<string>();

        //Open connection
        if (this.OpenConnection() == true)
        {
            //Create Command
            MySqlCommand cmd = new MySqlCommand(query, connection);
            //Create a data reader and Execute the command
            MySqlDataReader dataReader = cmd.ExecuteReader();

            //Read the data and store them in the list
            while (dataReader.Read())
            {
                list[0].Add(dataReader["id"] + "");
                list[1].Add(dataReader["name"] + "");
                list[2].Add(dataReader["age"] + "");
            }

            //close Data Reader
            dataReader.Close();

            //close Connection
            this.CloseConnection();

            //return list to be displayed
            return list;
        }
        else
        {
            return list;
        }
    }

    //Count statement
    public int Count()
    {
        string query = "SELECT Count(*) FROM tableinfo";
        int Count = -1;

        //Open Connection
        if (this.OpenConnection() == true)
        {
            //Create Mysql Command
            MySqlCommand cmd = new MySqlCommand(query, connection);

            //ExecuteScalar will return one value
            Count = int.Parse(cmd.ExecuteScalar() + "");

            //close Connection
            this.CloseConnection();

            return Count;
        }
        else
        {
            return Count;
        }
    }

    //Backup
    public void Backup()
    {
        try
        {
            DateTime Time = DateTime.Now;
            int year = Time.Year;
            int month = Time.Month;
            int day = Time.Day;
            int hour = Time.Hour;
            int minute = Time.Minute;
            int second = Time.Second;
            int millisecond = Time.Millisecond;

            //Save file to C:\ with the current date as a filename
            string path;
            path = "C:\\MySqlBackup" + year + "-" + month + "-" + day +
        "-" + hour + "-" + minute + "-" + second + "-" + millisecond + ".sql";
            StreamWriter file = new StreamWriter(path);


            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = "mysqldump";
            psi.RedirectStandardInput = false;
            psi.RedirectStandardOutput = true;
            psi.Arguments = string.Format(@"-u{0} -p{1} -h{2} {3}",
                uid, password, server, database);
            psi.UseShellExecute = false;

            Process process = Process.Start(psi);

            string output;
            output = process.StandardOutput.ReadToEnd();
            file.WriteLine(output);
            process.WaitForExit();
            file.Close();
            process.Close();
        }
        catch (IOException ex)
        {
            MessageBox.Show("Error , unable to backup!");
        }
    }

    //Restore
    public void Restore()
    {
        try
        {
            //Read file from C:\
            string path;
            path = "C:\\MySqlBackup.sql";
            StreamReader file = new StreamReader(path);
            string input = file.ReadToEnd();
            file.Close();

            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = "mysql";
            psi.RedirectStandardInput = true;
            psi.RedirectStandardOutput = false;
            psi.Arguments = string.Format(@"-u{0} -p{1} -h{2} {3}",
                uid, password, server, database);
            psi.UseShellExecute = false;


            Process process = Process.Start(psi);
            process.StandardInput.WriteLine(input);
            process.StandardInput.Close();
            process.WaitForExit();
            process.Close();
        }
        catch (IOException ex)
        {
            MessageBox.Show("Error , unable to Restore!");
        }
    }
}