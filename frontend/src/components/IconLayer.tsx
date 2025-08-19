import React, { useEffect, useState } from 'react';
import FloatingIcon from './FloatingIcon';

interface IconConfig {
  src: string;
  alt: string;
  width: number;
  height: number;
  left: string;
  top: string;
  rotate: string;
  transitionDelay?: number;
}

const iconConfigs: IconConfig[] = [
  {
    src: '/Images/Icons/upicon.png',
    alt: 'Up Icon',
    width: 60,
    height: 60,
    left: '3%',
    top: '2%',
    rotate: '-20deg',
    transitionDelay: 0,
  },
  {
    src: '/Images/Icons/upicon.png',
    alt: 'Down Icon',
    width: 60,
    height: 60,
    left: '90%',
    top: '10%',
    rotate: '-25deg',
    transitionDelay: 100,
  },
  {
    src: '/Images/Icons/upicon.png',
    alt: 'Star Icon',
    width: 50,
    height: 50,
    left: '67%',
    top: '30%',
    rotate: '0deg',
    transitionDelay: 200,
  },
  {
    src: '/Images/Icons/upicon.png',
    alt: 'Bolt Icon',
    width: 55,
    height: 55,
    left: '9%',
    top: '25%',
    rotate: '10deg',
    transitionDelay: 300,
  },
];

const IconLayer: React.FC = () => {
  const [stackIcons, setStackIcons] = useState<boolean>(false);

  useEffect(() => {
    const handleScroll = () => {
      const triggerPoint = 400;
      setStackIcons(window.scrollY > triggerPoint);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="relative w-full h-[100vh] overflow-hidden pointer-events-none" style={{ transform: 'translateY(-15%)' }}>
    {/* // <div className="relative w-full h-[100vh] overflow-hidden"> */}

      {iconConfigs.map((icon, index) => (
        <FloatingIcon
          key={index}
          {...icon}
          stacked={stackIcons}
          style={{
            transitionDelay: `${icon.transitionDelay || 10}ms`,
          }}
        />
      ))}
      <img
              src="/Images/Sttarkel_Student.png"
              alt="Career Icon"
              width={600}
              height={600}
              className="inline-block mt-2 mx-2 align-middle border-gray-200 border-opacity-60 rounded-xl left-1/6 top-1/2 opacity-100"
              style={{ verticalAlign: 'middle', offset: '50%', transform: 'translateY(48%)' }}
            />
    </div>
  );
};

export default IconLayer;















// import React, { useEffect, useState } from 'react';
// import FloatingIcon from './FloatingIcon';

// interface IconConfig {
//   src: string;
//   alt: string;
//   width: number;
//   height: number;
//   left: string;
//   top: string;
//   rotate: string;
// }

// const iconConfigs: IconConfig[] = [
//   {
//     src: '/Images/Icons/upicon.png',
//     alt: 'Up Icon',
//     width: 60,
//     height: 60,
//     left: '8%',
//     top: '2%',
//     rotate: '-20deg',
//   },
//   {
//     src: '/Images/Icons/upicon.png',
//     alt: 'Down Icon',
//     width: 60,
//     height: 60,
//     left: '90%',
//     top: '10%',
//     rotate: '-25deg',
//   },
//   {
//     src: '/Images/Icons/upicon.png',
//     alt: 'Star Icon',
//     width: 50,
//     height: 50,
//     left: '67%',
//     top: '30%',
//     rotate: '0deg',
//   },
//   {
//     src: '/Images/Icons/upicon.png',
//     alt: 'Bolt Icon',
//     width: 55,
//     height: 55,
//     left: '20%',
//     top: '20%',
//     rotate: '10deg',
//   },
// ];

// const IconLayer: React.FC = () => {
//   const [stackIcons, setStackIcons] = useState<boolean>(false);

//   useEffect(() => {
//     const handleScroll = () => {
//       const triggerPoint = 400; // Adjust based on your layout
//       setStackIcons(window.scrollY > triggerPoint);
//     };

//     window.addEventListener('scroll', handleScroll);
//     return () => window.removeEventListener('scroll', handleScroll);
//   }, []);

//   return (
//     <div className="relative w-full h-[100vh] overflow-hidden" style={{ transform: 'translateY(-15%)' }}>
//       {iconConfigs.map((icon, index) => (
//         <FloatingIcon key={index} {...icon} stacked={stackIcons} />
//       ))}
//     </div>
//   );
// };

// export default IconLayer;
