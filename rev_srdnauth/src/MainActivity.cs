using System;
using Android.App;
using Android.OS;
using Android.Runtime;
using Android.Widget;
using AndroidX.AppCompat.App;

namespace SrdnAuth
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true)]
    public class MainActivity : AppCompatActivity
    {
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            Xamarin.Essentials.Platform.Init(this, savedInstanceState);
            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.activity_main);

            // Get our UI controls from the loaded layout
            
            EditText flagEditText = FindViewById<EditText>(Resource.Id.FlagEditText);
            TextView outputTextView = FindViewById<TextView>(Resource.Id.OutputTextView);
            Button buttonCheckFlag = FindViewById<Button>(Resource.Id.ButtonCheckFlag);

            buttonCheckFlag.Click += (s, e) =>
            {
                string output = Core.FlagChecker.Check(flagEditText.Text);
                outputTextView.Text= output;
            };
            
        }
        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, [GeneratedEnum] Android.Content.PM.Permission[] grantResults)
        {
            Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);

            base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }
}